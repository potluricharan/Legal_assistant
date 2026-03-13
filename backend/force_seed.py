import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- PATH LOGIC ---
# This looks in the SAME folder where THIS script is saved
base_path = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(base_path, "serviceAccountKey.json")

print(f"Searching for key at: {key_path}")

# 1. Check if the file exists
if not os.path.exists(key_path):
    print("ERROR: Still can't find the file!")
    print("--- DEBUG STEPS ---")
    print(f"1. Open this folder in your File Explorer: {base_path}")
    print("2. Ensure 'serviceAccountKey.json' is sitting RIGHT THERE.")
    print("3. Check for double extensions (e.g., serviceAccountKey.json.json)")
    exit(1)

# 2. Initialize Firebase
try:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Connected to Firebase successfully!")

    # 3. Seed the Data
    collections = {
        "lawyers": {"name": "Vikram Desai", "status": "Verified"},
        "cases": {"caseId": "CASE-101", "title": "System Test"},
        "evidence": {"type": "Mobile Forensics", "id": "EVD-001"}
    }

    for col, data in collections.items():
        db.collection(col).add(data)
        print(f"✅ Created collection: {col}")

    print("\nSUCCESS: All collections are now live in Firebase!")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")