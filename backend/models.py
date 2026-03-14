from datetime import datetime, timezone

class FirebaseSchema:
    """Defines the NoSQL document structures for Firestore to ensure consistency."""
    
    @staticmethod
    def create_case_doc(filename, summary, prediction_text, file_url):
        """Schema for the main case document stored in the 'cases' collection."""
        return {
            "filename": filename,
            "initial_summary": summary,
            "current_summary": summary,
            "file_url": file_url,
            "status": "Active",
            "created_at": datetime.now(timezone.utc),
            "last_updated": datetime.now(timezone.utc),
            "latest_prediction": prediction_text
        }

    @staticmethod
    def create_history_entry(event_type, content, ai_delta=""):
        """Schema for the history log stored in the 'case_history' sub-collection."""
        return {
            "type": event_type,  # Examples: 'CHAT', 'WITNESS_ADDED', 'DOCUMENT_UPDATE'
            "content": content,
            "ai_delta": ai_delta,
            "timestamp": datetime.now(timezone.utc)
        }