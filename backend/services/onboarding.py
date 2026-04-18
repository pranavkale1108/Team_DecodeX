import networkx as nx

def generate_onboarding_path(parsed_files: list, G: nx.DiGraph) -> list:
    path = []
    # Identify entry points typical to Python projects
    entry_candidates = ["main.py", "app.py", "index.py", "run.py", "manage.py", "setup.py", "__init__.py"]
    
    entry_points = []
    for f in parsed_files:
        basename = f["name"].split('/')[-1]
        if basename in entry_candidates:
            entry_points.append(f["name"])
            
    # Identify most connected files (highest in-degree: used by many things)
    in_degrees = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)
    important_files = [node for node, degree in in_degrees if degree > 0][:5]
    
    # Combine entry points and important files
    for ep in entry_points:
        if ep not in path:
            path.append(ep)
            
    for ipf in important_files:
        if ipf not in path:
            path.append(ipf)
            
    # Add a few remaining core files up to 10
    for f in parsed_files:
        if f["name"] not in path and len(path) < 10:
            path.append(f["name"])
            
    return path
