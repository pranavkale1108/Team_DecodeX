import datetime
from backend.config.db import repositories_collection

def get_repository_by_url(repo_url: str):
    return repositories_collection.find_one({"repo_url": repo_url}, {"_id": 0})

def save_repository_data(repo_url: str, repo_name: str, graph: dict, files: list, onboarding_path: list):
    document = {
        "repo_url": repo_url,
        "repo_name": repo_name,
        "graph": graph,
        "files": files,
        "onboarding_path": onboarding_path,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    # Update if exists, or insert
    repositories_collection.update_one(
        {"repo_url": repo_url},
        {"$set": document},
        upsert=True
    )
    return document

def get_graph_by_url(repo_url: str):
    repo = repositories_collection.find_one({"repo_url": repo_url}, {"_id": 0, "graph": 1})
    return repo.get("graph") if repo else None

def get_file_info(repo_url: str, file_name: str):
    repo = repositories_collection.find_one({"repo_url": repo_url}, {"_id": 0, "files": 1})
    if repo and "files" in repo:
        for file in repo["files"]:
            if file["name"] == file_name:
                return file
    return None

def get_onboarding_path(repo_url: str):
    repo = repositories_collection.find_one({"repo_url": repo_url}, {"_id": 0, "onboarding_path": 1})
    return repo.get("onboarding_path") if repo else None
