import os
import ollama

def generate_file_summary(file_data: dict) -> str:
    """Generate a 2-3 line summary of what the file does."""
    prompt = f"Analyze this Python file based on its metadata:\nFile: {file_data['name']}\nImports: {', '.join(file_data['imports'])}\nClasses: {', '.join(file_data['classes'])}\nFunctions: {', '.join(file_data['functions'])}\n\nProvide a concise 2-3 line summary of its purpose or role."
    
    try:
        response = ollama.chat(
            model='llama3:8b',
            messages=[
                {"role": "system", "content": "You are an expert Python developer. Be concise."},
                {"role": "user", "content": prompt}
            ],
            options={'num_predict': 100, 'temperature': 0.3}
        )
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Error generating summary for {file_data['name']}: {e}")
        return f"File dealing with imports: {', '.join(file_data['imports'][:3])} and containing {len(file_data['functions'])} functions."

def query_repository(query: str, repo_context: str) -> str:
    prompt = f"You are CodeAtlas, an AI assistant for evaluating a codebase.\nContext of the repository files:\n{repo_context}\n\nUser query: {query}\nProvide a helpful, precise answer."
    
    try:
        response = ollama.chat(
            model='llama3:8b',
            messages=[
                {"role": "system", "content": "You are a helpful assistant evaluating a codebase architecture. Answer in markdown if appropriate. Be concise."},
                {"role": "user", "content": prompt}
            ],
            options={'temperature': 0.3}
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error answering query: {str(e)}. Make sure Ollama is running with 'ollama serve' and the model is pulled with 'ollama pull llama3:8b'."
