# **Capstone Project Part 1: Project Roadmap**

**Project Title:** The AI Mood-Jockey

## **1\. The Project Idea**

**Concept:**

The AI Mood-Jockey is a web application designed to bridge the gap between human emotion and music discovery. While standard streaming platforms require specific genre or artist searches, this application allows users to input natural language descriptions of their current state (e.g., *"I'm stressed about finals and need to focus"*).

The application validates the "uniqueness" criterion by using Generative AI (LLM) to act as a semantic translator, converting vague human feelings into precise database queries to fetch relevant music.

## **2\. Main Features**

To ensure the project remains feasible within the timeline, the scope is limited to these core functionalities:

* **Natural Language Input:** A simple front-end interface accepting text input describing feelings, weather, or activities.  
* **AI Context Analysis:** A backend process that interprets the input and extracts 2-3 musical parameters (Genre, Valence/Mood, Tempo).  
* **Smart Music Retrieval:** A search engine that uses the extracted parameters to fetch real songs from Jamendo.  
* **Visual Playlist Feed:** A results page displaying album art, track titles, and artist names.  
* **Audio Preview:** Integration of 30-second audio previews for immediate listening.

## **3\. Selected APIs**

Two external APIs are required to make this system work:

**A. Google Gemini API (The Intelligence)**

* **Role:** Analyzes the user's text prompt.  
* **Data Provided:** Returns a JSON object containing suggested genres (e.g., "lo-fi", "jazz") and keywords (e.g., "study", "focus").  
* **Cost:** Free tier.

**B. Jamendo API (The Data)**

* **Role:** Provides the actual song library and audio files.  
* **Data Provided:** Track names, artists, album images, and direct MP3 preview URLs.  
* **Endpoint:** `GET /v1.0/tracks/` (Using `fuzzytags` and `boost` for mood-based results).  
* **Auth Method:** Client ID (Simple API Key).

## **4\. Django Apps & Endpoints Plan**

To maintain modularity and separation of concerns, the project will be divided into two specific Django apps.

### **App 1: web\_interface**

* **Responsibility:** Handles the user-facing HTML pages, static files, and form rendering.  
* **Endpoints:**  
  * GET / : Renders the Homepage (Input Form).  
  * GET /history/ : (Optional) Renders a list of past searches.

### **App 2: playlist\_generator**

* **Responsibility:** Handles the business logic, API communication, and data processing.  
* **Endpoints:**  
  * POST /generate/ : Accepts form data, triggers the AI \+ Jamendo chain, and returns the results template.

## **5\. Database Schema Design**

The project uses a relational database to store user interactions.

### **Model: MoodQuery**

This model records the "translation" process from human text to AI data.

| **Field Name** | **Data Type** | **Constraints** | **Description** |

| id | AutoField | Primary Key | Unique ID. |

| user\_input | CharField | Max Length: 500 | The raw text typed by the user. |

| generated\_keywords | JSONField | Null=True | The keywords extracted by Gemini. |

| created\_at | DateTimeField | Auto\_now\_add=True | Timestamp of the query. |

* **Relationships:** A `ForeignKey` to the Django `User` model is required to link queries to specific user accounts for history tracking.  
* **Constraint:** user\_input cannot be empty.

## **6\. Implementation Plan (Phased Roadmap)**

**Phase 1: Setup & API Verification**

* Initialize the Django project and create the two apps (web\_interface, playlist\_generator).  
* Register for Jamendo Developer keys and Gemini API keys.  
* **Security:** Use `python-dotenv` to manage API keys securely in a `.env` file.
* **Deliverable:** A python script that successfully prints 5 songs from Jamendo in the terminal.

**Phase 2: Backend Logic (The "playlist\_generator" App)**

* Build the service layer that calls Gemini.  
* **AI Validation:** Use Gemini's "JSON Mode" and implement `try/except` blocks to handle malformed AI responses.
* Connect the AI output to the Jamendo `recommendations` endpoint.  
* **Deliverable:** The backend logic receives "Sad" and returns a list of sad song objects.

**Phase 3: Database & Views**

* Implement the MoodQuery and User models and run migrations.  
* Create the Django Views to handle the POST request from the frontend.  
* Save every search to the database, linked to the logged-in user.  
* **Deliverable:** A basic HTML page where typing in a box and clicking submit reloads the page with raw data.

**Phase 4: Frontend Implementation**

* Install a CSS framework (Bootstrap or Tailwind).  
* Design the Result Cards (Image \+ Title \+ Artist).  
* **UX:** Implement a loading spinner/animation to provide feedback during the 2-5 second API wait time.
* Add the "Play Preview" functionality.  
* **Deliverable:** A polished, responsive user interface.

**Phase 5: Testing & Finalization**

* Add error handling (e.g., "What if Jamendo is down?").  
* Clean up code and write comments.  
* Record the demo video.  
* **Deliverable:** Final Project Submission.
