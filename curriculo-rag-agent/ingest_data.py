import json
import os
import urllib.request

API_URL = "http://localhost:8010/api/v1/ingest"
DATA_DIR = "data"

files = [
    "rag_tutorial_simplilearn.txt",
    "agentic_ai_coding.txt",
    "ai_agents_overview.txt",
    "scalable_rag_kamradt.txt"
]

def ingest():
    for filename in files:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
            
        with open(path, "r") as f:
            content = f.read()
            
        print(f"Ingesting {filename}...")
        data = json.dumps({"text": content, "source": filename}).encode('utf-8')
        
        req = urllib.request.Request(
            API_URL, 
            data=data, 
            headers={'Content-Type': 'application/json'}
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                print(f"Response: {response.status} - {response.read().decode()}")
        except Exception as e:
            print(f"Error ingesting {filename}: {e}")

if __name__ == "__main__":
    ingest()
