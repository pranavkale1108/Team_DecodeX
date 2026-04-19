import os
import ast

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".json",
    ".md", ".rst", ".toml", ".yaml", ".yml", ".ini", ".cfg", ".txt"
}

EXCLUDED_DIRS = {
    ".git", ".github", "__pycache__", "node_modules", ".venv", "venv",
    "env", "dist", "build", ".mypy_cache", ".pytest_cache"
}

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

def parse_generic_file(file_path: str, base_path: str) -> dict:
    rel_path = os.path.relpath(file_path, base_path)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read(20000)
    except OSError:
        source = ""

    return {
        "name": rel_path.replace('\\', '/'),
        "imports": [],
        "functions": [],
        "classes": [],
        "secrets_found": any(keyword in source.lower() for keyword in ["api_key", "secret", "password"])
    }

def scan_repository(local_path: str) -> list:
    files_data = []
    for root, dirs, files in os.walk(local_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('.')]
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1].lower()
            if extension in SUPPORTED_EXTENSIONS:
                if extension == ".py":
                    parsed_data = parse_python_file(file_path, local_path)
                else:
                    parsed_data = parse_generic_file(file_path, local_path)
                if parsed_data:
                    files_data.append(parsed_data)
    return files_data
