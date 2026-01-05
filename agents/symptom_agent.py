class SymptomAnalysisAgent:
    def __init__(self):
        pass

    def analyze(self, user_text):
        """
        Extracts symptoms and determines severity from user text.
        Simple rule-based extraction for demo purposes.
        """
        user_text = user_text.lower()
        
        # Keyword dictionary for extraction
        common_symptoms = [
            "redness", "itching", "discharge", "tearing", "pain",
            "blurred vision", "halos", "tunnel vision", "clouded", 
            "light sensitivity", "spots", "floaters", "vision loss"
        ]
        
        extracted = [s for s in common_symptoms if s in user_text]
        
        # Simple severity logic
        severity = "Low"
        high_severity_keywords = ["pain", "vision loss", "sudden", "severe", "dark"]
        
        if any(w in user_text for w in high_severity_keywords):
            severity = "High"
        elif len(extracted) > 3:
            severity = "Medium"
            
        return {
            "symptoms": extracted,
            "severity": severity,
            "original_text": user_text
        }
