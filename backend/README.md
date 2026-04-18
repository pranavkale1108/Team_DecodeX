# CodeAtlas Backend

An AI-powered Repository Architecture Navigator backend.

## Architecture & Features
- **Repository Ingestion:** Clones GitHub repos efficiently via `GitPython`.
- **Parsing Engine:** Uses `ast` to map out functions, classes, and dependencies in Python code.
- **Graphing:** Models dependencies using `NetworkX` identifying important/central modules.
- **AI Integration:** Ties into `OpenAI` to generate file summaries and answer high-level structural queries in natural language.
- **Optimized Caching:** Results are heavily cached in a MongoDB `codeatlas` database via `pymongo` avoiding unnecessary recomputations.
- **Bonus:** Included basic secrets scanning and graph centrality file importance scores.

## Tech Stack
- Python 3.9+ 
- FastAPI
- MongoDB (via PyMongo)
- NetworkX
- OpenAI
- GitPython

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   A `.env` file must be present in the `backend` directory:
   ```env
   MONGO_URI=mongodb://localhost:27017
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Start MongoDB:**
   Ensure MongoDB service is running locally on port `27017` (or updated according to `.env`).

4. **Run Server:**
   Launch the FastAPI application:
   ```bash
   # From the root directory (Team_DecodeX) run:
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Endpoints

- `POST /api/analyze-repo` - Instructs the backend to analyze a GitHub repository. Expected payload: `{"repo_url": "..."}`
- `GET /api/graph?repo_url=...` - Retrives JSON-formatted file graph 
- `GET /api/file-info?repo_url=...&file_name=...` - Returns extracted file metadata and dependencies
- `POST /api/query` - Queries the AI based on repo context. Expected Payload: `{"repo_url": "...", "query": "..."}`
- `GET /api/onboarding-path?repo_url=...` - Serves out an optimal reading/onboarding path for newcomers.

## Interactive Documentation
When running locally, check out the Swagger API Documentation at: 
[http://localhost:8000/docs](http://localhost:8000/docs)
