from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import backend.services.db_service as db_service
from backend.services.repo_handler import clone_repository, cleanup_repository, get_repo_name
from backend.services.parser import scan_repository
from backend.services.graph_builder import build_dependency_graph
from backend.services.ai_service import generate_file_summary, query_repository
from backend.services.onboarding import generate_onboarding_path

router = APIRouter()

class RepoRequest(BaseModel):
    repo_url: str

class QueryRequest(BaseModel):
    repo_url: str
    query: str

@router.post("/analyze-repo")
async def analyze_repo(request: RepoRequest):
    repo_url = request.repo_url
    
    # Check if already exists in MongoDB
    existing_repo = db_service.get_repository_by_url(repo_url)
    if existing_repo:
        return {"status": "success", "message": "Repository fetched from DB", "data": existing_repo}
        
    try:
        # 1. Clone repo
        local_path = clone_repository(repo_url)
        repo_name = get_repo_name(repo_url)
        
        # 2. Parse code
        parsed_files = scan_repository(local_path)
        
        # 3. Build graph
        graph_data, G = build_dependency_graph(parsed_files)
        
        # 4. Generate AI specific data & populate final files structure
        final_files = []
        for f in parsed_files:
            summary = generate_file_summary(f)
            file_info = {
                "name": f["name"],
                "dependencies": [v for u, v in G.edges() if u == f["name"]],
                "used_by": [u for u, v in G.edges() if v == f["name"]],
                "summary": summary,
                "secrets_found": f.get("secrets_found", False)
            }
            final_files.append(file_info)
            
        # 5. Generate onboarding path
        onboarding_path = generate_onboarding_path(parsed_files, G)
        
        # 6. Save to DB
        saved_data = db_service.save_repository_data(
            repo_url=repo_url,
            repo_name=repo_name,
            graph=graph_data,
            files=final_files,
            onboarding_path=onboarding_path
        )
        saved_data.pop("_id", None) # Remove ObjectID for JSON serialization if present
        
        # Cleanup
        cleanup_repository(local_path)
        
        return {"status": "success", "message": "Repository analyzed and saved", "data": saved_data}
        
    except Exception as e:
        if 'local_path' in locals():
            cleanup_repository(local_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/graph")
def get_graph(repo_url: str):
    graph = db_service.get_graph_by_url(repo_url)
    if not graph:
        raise HTTPException(status_code=404, detail="Repository not found in DB")
    return {"status": "success", "graph": graph}

@router.get("/file-info")
def get_file_information(repo_url: str, file_name: str):
    file_info = db_service.get_file_info(repo_url, file_name)
    if not file_info:
        raise HTTPException(status_code=404, detail="File info not found")
    return {"status": "success", "file": file_info}

@router.post("/query")
def query_repo(request: QueryRequest):
    repo_data = db_service.get_repository_by_url(request.repo_url)
    if not repo_data:
        raise HTTPException(status_code=404, detail="Repository not found in DB")
        
    # Compress context to just files and summaries to fit prompt limits
    context_lines = []
    for f in repo_data.get("files", []):
        context_lines.append(f"{f['name']}: {f['summary']}")
    repo_context = "\n".join(context_lines)
    
    answer = query_repository(request.query, repo_context)
    return {"status": "success", "answer": answer}

@router.get("/onboarding-path")
def get_onboarding(repo_url: str):
    path = db_service.get_onboarding_path(repo_url)
    if not path:
        raise HTTPException(status_code=404, detail="Onboarding path not found")
    return {"status": "success", "onboarding_path": path}
