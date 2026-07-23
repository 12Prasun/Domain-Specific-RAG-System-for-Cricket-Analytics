import os
import requests
from flask import Flask, request, Response
from dotenv import load_dotenv

load_dotenv(override=True)
app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GOOGLE_OPENAI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/openai"

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
@app.route('/chat/completions', methods=['POST', 'OPTIONS'])
def chat_completions():
    if request.method == 'OPTIONS':
        return Response(status=200)
    
    data = request.get_json(force=True)
    
    # The magic happens here: We rewrite the model requested by your code to a Gemini model!
    if data.get('model') == 'gpt-3.5-turbo':
        data['model'] = 'gemini-3.1-flash-lite'
    
    # Prepare headers, injecting your real Gemini API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    
    # Forward the modified request to Google's OpenAI-compatible endpoint
    target_url = f"{GOOGLE_OPENAI_ENDPOINT}/chat/completions"
    resp = requests.post(target_url, json=data, headers=headers, stream=True)
    
    # Return the exact response back to LangChain
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]
    
    return Response(resp.iter_content(chunk_size=10*1024),
                    status=resp.status_code,
                    headers=response_headers)

if __name__ == '__main__':
    print("Gemini Translation Proxy started on port 4000!")
    app.run(port=4000, host="0.0.0.0")
