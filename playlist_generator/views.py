import json
import logging
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import MoodQuery, Track
from .services import JamendoService
from .ai_service import GeminiService

logger = logging.getLogger(__name__)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_status(request):
    """Public endpoint to check API status."""
    return JsonResponse({
        "status": "active",
        "service": "Mood-Jockey API",
        "endpoints": {
            "status": "/api/status/",
            "public_generate": "/api/public/generate/"
        }
    })

@csrf_exempt
@require_http_methods(["POST"])
def public_generate_playlist(request):
    """Public version of the generate_playlist endpoint for testing/course submission."""
    try:
        data = json.loads(request.body)
        user_input = data.get('user_input', '')
        
        if not user_input:
            return JsonResponse({'error': 'User input is required'}, status=400)

        # 1. Analyze mood with Gemini
        ai_response = GeminiService.analyze_mood(user_input)
        if 'error' in ai_response:
            return JsonResponse(ai_response, status=500)
            
        genres = ai_response.get('genres', [])
        moods = ai_response.get('moods', [])
        keywords = ai_response.get('keywords', [])
        
        # 2. Fetch tracks from Jamendo
        jamendo_tracks = JamendoService.get_tracks(genres, moods, keywords, limit=10)
        
        if not jamendo_tracks:
            return JsonResponse({'error': 'No tracks found for the given mood'}, status=404)

        # 3. Format response (Skip saving to DB for public/anonymous testing if desired, or save to a default 'anonymous' user)
        # For simplicity in this public test, we just return the tracks without saving to DB history.
        
        return JsonResponse({
            'message': 'Public test successful',
            'user_input': user_input,
            'keywords': ai_response,
            'tracks': jamendo_tracks
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception("An error occurred during public playlist generation")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

@login_required
@require_http_methods(["POST"])
def generate_playlist(request):
    try:
        data = json.loads(request.body)
        user_input = data.get('user_input', '')
        
        if not user_input:
            return JsonResponse({'error': 'User input is required'}, status=400)

        # 1. Analyze mood with Gemini
        ai_response = GeminiService.analyze_mood(user_input)
        if 'error' in ai_response:
            return JsonResponse(ai_response, status=500)
            
        genres = ai_response.get('genres', [])
        moods = ai_response.get('moods', [])
        keywords = ai_response.get('keywords', [])
        
        # 2. Fetch tracks from Jamendo using tiered search strategy
        jamendo_tracks = JamendoService.get_tracks(genres, moods, keywords, limit=24)
        
        if not jamendo_tracks:
            return JsonResponse({'error': 'No tracks found for the given mood'}, status=404)

        # 3. Save to database
        mood_query = MoodQuery.objects.create(
            user=request.user,
            user_input=user_input,
            generated_keywords=ai_response
        )

        saved_tracks = []
        for track_data in jamendo_tracks:
            track, created = Track.objects.get_or_create(
                jamendo_id=track_data['id'],
                defaults={
                    'title': track_data['title'],
                    'artist': track_data['artist'],
                    'preview_url': track_data['preview_url'],
                    'album_image': track_data.get('album_image', '')
                }
            )
            mood_query.tracks.add(track)
            
            # Add to response
            track_dict = {
                'id': track.id,
                'jamendo_id': track.jamendo_id,
                'title': track.title,
                'artist': track.artist,
                'preview_url': track.preview_url,
                'album_image': track.album_image
            }
            saved_tracks.append(track_dict)
            
        return JsonResponse({
            'query_id': mood_query.id,
            'user_input': mood_query.user_input,
            'keywords': mood_query.generated_keywords,
            'tracks': saved_tracks
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.exception("An error occurred during playlist generation")
        return JsonResponse({'error': 'An unexpected error occurred while generating your playlist.'}, status=500)

@login_required
@require_http_methods(["GET"])
def get_query(request, query_id):
    query = get_object_or_404(MoodQuery, id=query_id, user=request.user)
    tracks = [{
        'id': t.id,
        'title': t.title,
        'artist': t.artist,
        'preview_url': t.preview_url,
        'album_image': t.album_image
    } for t in query.tracks.all()]
    
    return JsonResponse({
        'query_id': query.id,
        'user_input': query.user_input,
        'keywords': query.generated_keywords,
        'created_at': query.created_at.isoformat(),
        'tracks': tracks
    })

@login_required
@require_http_methods(["DELETE"])
def delete_query(request, query_id):
    query = get_object_or_404(MoodQuery, id=query_id, user=request.user)
    query.delete()
    return JsonResponse({'success': True, 'message': 'Query deleted successfully'})
