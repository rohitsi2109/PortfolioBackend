# Portfolio AI Backend

This is the FastAPI backend for Rohit Singh's portfolio. It powers the "Chat with AI" feature using a Retrieval-Augmented Generation (RAG) system.

## Features
- **FastAPI**: High-performance Python web framework.
- **RAG Architecture**: Uses **LanceDB** to store and retrieve relevant context from the portfolio profile.
- **AI Model**: Integrated with **Google Gemini 1.5 Flash** for intelligent responses.
- **Elite Persona**: The AI is prompted to act as a professional agent representing Rohit to recruiters.

## Setup

1.  **Clone the repository** (if not already done).
2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python -m venv myenv
    # Windows
    myenv\Scripts\activate
    # Mac/Linux
    source myenv/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Environment Variables**:
    Create a `.env` file in this directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## Running the Server

Run the development server:
```bash
fastapi dev main.py
```
The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

-   **POST** `/chat`: 
    -   Input: `{"question": "Tell me about Rohit's experience."}`
    -   Output: `{"answer": "..."}`
-   **GET** `/health`: 
    -   Returns system status and RAG readiness.
