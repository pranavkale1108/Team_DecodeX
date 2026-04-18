import networkx as nx

def build_dependency_graph(parsed_files: list) -> tuple:
    G = nx.DiGraph()
    
    # Map module names to file paths heuristically to link intra-repo dependencies
    module_to_file = {}
    for f in parsed_files:
        name = f["name"]
        G.add_node(name)
        
        # e.g. backend/services/parser.py -> backend.services.parser or parser
        mod_name = name.replace('/', '.').replace('\\', '.').replace('.py', '')
        module_to_file[mod_name] = name
        
        # also map just the basename
        basename = name.split('/')[-1].replace('.py', '')
        if basename not in module_to_file: # keep the first one
            module_to_file[basename] = name

    for f in parsed_files:
        name = f["name"]
        for imp in f["imports"]:
            # If the imported module matches one of our local files
            for mod_key in module_to_file:
                if imp == mod_key or imp.startswith(mod_key + '.') or mod_key.endswith(imp): # heuristic
                   target_file = module_to_file[mod_key]
                   if target_file != name:
                       G.add_edge(name, target_file)
                       break
                       
    # Calculate Importance Score for files based on in-degree centrality (Bonus)
    centrality = nx.in_degree_centrality(G)
    nodes = [{"id": node, "importance": centrality.get(node, 0)} for node in G.nodes()]
    edges = [{"source": u, "target": v} for u, v in G.edges()]
    
    return {"nodes": nodes, "edges": edges}, G
