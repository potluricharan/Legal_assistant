import os
from google import genai
from dotenv import load_dotenv

def test_connection():
    # 1. Load the .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file!")
        return

    # 2. Initialize the New Client
    client = genai.Client(api_key=api_key)

    print("--- Testing Connection (New SDK) ---")
    try:
        # 3. Try a simple prompt using gemini-1.5-flash
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Say 'The legal system is ready' if you can hear me."
        )
        print(f"✅ Success! Gemini says: {response.text}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()