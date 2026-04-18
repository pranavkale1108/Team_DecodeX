import os
import openai

def generate_file_summary(file_data: dict) -> str:
    """Generate a 2-3 line summary of what the file does."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return f"File dealing with imports: {', '.join(file_data['imports'][:3])} and containing {len(file_data['functions'])} functions."
        
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"Analyze this Python file based on its metadata:\nFile: {file_data['name']}\nImports: {', '.join(file_data['imports'])}\nClasses: {', '.join(file_data['classes'])}\nFunctions: {', '.join(file_data['functions'])}\n\nProvide a concise 2-3 line summary of its purpose or role."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Python developer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating summary for {file_data['name']}: {e}")
        return "Error generating summary."

def query_repository(query: str, repo_context: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return "AI query currently not available (API key missing)."
        
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"You are CodeAtlas, an AI assistant for evaluating a codebase.\nContext of the repository files:\n{repo_context}\n\nUser query: {query}\nProvide a helpful, precise answer."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # standard model
            messages=[
                {"role": "system", "content": "You are a helpful assistant evaluating a codebase architecture. Answer in markdown if appropriate."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error answering query: {str(e)}"
