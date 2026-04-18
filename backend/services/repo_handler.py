import os
import shutil
from git import Repo
import uuid
import re

REPOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "repos")

def get_repo_name(repo_url: str) -> str:
    # Extracts name from something like https://github.com/user/repo_name.git
    match = re.search(r'/([^/]+)(?:\.git)?$', repo_url)
    if match:
        return match.group(1).replace('.git', '')
    return "unknown_repo"

def clone_repository(repo_url: str) -> str:
    if not os.path.exists(REPOS_DIR):
        os.makedirs(REPOS_DIR)
        
    unique_id = str(uuid.uuid4())[:8]
    repo_name = get_repo_name(repo_url)
    local_path = os.path.join(REPOS_DIR, f"{repo_name}_{unique_id}")
    
    Repo.clone_from(repo_url, local_path)
    return local_path

def cleanup_repository(local_path: str):
    if os.path.exists(local_path):
        import stat
        def rmtree_error_handler(func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            func(path)
        shutil.rmtree(local_path, onerror=rmtree_error_handler)
