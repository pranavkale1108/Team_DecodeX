import os
from google import genai  # Replaced 'import openai'

def generate_file_summary(file_data: dict) -> str:
    """Generate a 2-3 line summary of what the file does."""
    # 1. Update the environment variable key
    api_key = os.getenv("GEMINI_API_KEY") 
    
    if not api_key or api_key == "your_gemini_api_key_here":
        # Keep your existing fallback logic
        return f"File dealing with imports: {', '.join(file_data.get('imports', []))}"
    
    # 2. Initialize the Gemini client
    client = genai.Client(api_key=api_key)

    prompt = f"Analyze this Python file based on its metadata..." # (Keep your existing prompt)

    try:
        # 3. Call the Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        # 4. Return the generated text
        return response.text
        
    except Exception as e:
        return f"Error generating summary: {e}"

def query_repository(query: str, repo_context: str) -> str:
    """Answer questions about the repository using AI."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "AI Query unavailable: API Key missing."
    
    client = genai.Client(api_key=api_key)
    prompt = f"You are CodeAtlas AI. Answer the following question about the codebase provided in the context.\n\nCODEBASE CONTEXT:\n{repo_context}\n\nQUESTION: {query}"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error querying repository: {e}"