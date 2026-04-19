import os
import sys
sys.path.append(os.getcwd())
from backend.services.parser import scan_repository
from backend.services.graph_builder import build_dependency_graph

def main():
    # Scan the backend directory
    local_path = os.getcwd()
    backend_path = os.path.join(local_path, 'backend')
    
    if not os.path.exists(backend_path):
        print(f"Error: {backend_path} not found")
        return

    parsed_files = scan_repository(backend_path)
    graph_data, G = build_dependency_graph(parsed_files)

    print(f"\nAnalysis for: {backend_path}")
    print(f"Total Nodes: {len(graph_data['nodes'])}")
    print(f"Total Edges: {len(graph_data['edges'])}\n")
    
    print("Connection Edges:")
    for edge in graph_data['edges']:
        print(f" {edge['source']}  --->  {edge['target']}")

if __name__ == '__main__':
    main()
