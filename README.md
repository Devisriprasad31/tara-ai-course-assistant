# Tara AI Course Assistant - Production Ready

Tara is an AI-powered e-learning assistant built with a FastAPI backend (using FAISS and Gemini RAG pipeline) and a React + Vite frontend.

## Project Structure
- `backend/` - Contains the FastAPI application, vector store, and AI ingestion scripts.
- `frontend/` - Contains the React + Vite application for the chat interface.

## Local Setup

### 1. Prerequisites
- Python 3.10+
- Node.js 20.17+
- A Google Gemini API Key

### 2. Backend Setup
1. Open a terminal and navigate to the project root.
2. Create and activate a virtual environment (e.g., `python -m venv .venv`).
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Configure environment variables in `backend/.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   FRONTEND_URL=http://localhost:5173
   ```
5. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   *Note: Use `--reload` flag for development auto-reloading.*

### 3. Frontend Setup
1. Open a second terminal.
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Create `frontend/.env` based on `frontend/.env.example`:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
5. Start the Vite development server:
   ```bash
   npm run dev
   ```

## Knowledge Base Ingestion

You can dynamically update the FAISS vector database without wiping existing data. Use the `update_knowledge.py` script provided in the backend folder.
*Note: Ensure the backend is restarted after appending new data to load it into memory.*

```bash
cd backend
python update_knowledge.py --json data/new_courses.json
python update_knowledge.py --pdf my_document.pdf
```

## Production Deployment Notes

### Backend Deployment (e.g., Render, Google Cloud Run)
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend/`
- Ensure you set the `GEMINI_API_KEY` and `FRONTEND_URL` environment variables in your hosting provider's dashboard.
- The `vector_store/` must be mounted on a persistent disk or cloud storage if you wish to retain dynamic ingestions across restarts.

### Frontend Deployment (e.g., Vercel, Netlify)
- **Build Command**: `npm run build`
- **Publish Directory**: `dist/`
- Ensure you set the `VITE_API_URL` environment variable to your production backend URL (e.g., `https://tara-backend.render.com`).
