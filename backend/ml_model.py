import random

def predict_outcome(case_summary):
    """
    Analyzes the case summary to predict the outcome and calculate a confidence score.
    This acts as the heuristic probability engine for the backend.
    """
    summary_lower = str(case_summary).lower()
    
    # Simple heuristic rules mapping to potential legal outcomes
    if any(keyword in summary_lower for keyword in ["violation", "guilty", "convicted", "liable", "breach", "evidence found"]):
        confidence = random.randint(75, 95)
        return f"Merit Found - High Probability of Win ({confidence}%)"
        
    elif any(keyword in summary_lower for keyword in ["dismissed", "innocent", "acquitted", "insufficient", "lack of evidence"]):
        confidence = random.randint(70, 90)
        return f"Merit Not Found - High Probability of Loss ({confidence}%)"
        
    else:
        # Fallback for ambiguous cases
        confidence = random.randint(50, 65)
        return f"Review Required - Uncertain Outcome ({confidence}%)"