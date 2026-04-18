import os
import ast

def parse_python_file(file_path: str, base_path: str) -> dict:
    rel_path = os.path.relpath(file_path, base_path)
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None  # Ignore files that fail to parse
        
    imports = []
    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
            
    # Basic secrets detection functionality (Bonus)
    secrets_found = False
    if any(keyword in source.lower() for keyword in ["api_key", "secret", "password"]):
        secrets_found = True
            
    return {
        "name": rel_path.replace('\\', '/'),
        "imports": list(set(imports)),
        "functions": functions,
        "classes": classes,
        "secrets_found": secrets_found
    }

def scan_repository(local_path: str) -> list:
    files_data = []
    for root, dirs, files in os.walk(local_path):
        # Exclude hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                parsed_data = parse_python_file(file_path, local_path)
                if parsed_data:
                    files_data.append(parsed_data)
    return files_data
