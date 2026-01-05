class Scorer:
    @staticmethod
    def normalize(score, min_val=0, max_val=100):
        """Normalizes a score to 0-1 range."""
        return (score - min_val) / (max_val - min_val) if max_val > min_val else 0

    @staticmethod
    def calculate_confidence(symptom_match, rag_relevance, web_val):
        """
        Calculates weighted confidence.
        Weights: 0.4 symptom, 0.4 rag, 0.2 web
        """
        # Ensure inputs are 0-100 based or normalized
        # We assume inputs might be 0-1 or 0-100, let's standardize to 0-1 float for calculation
        
        s = symptom_match if symptom_match <= 1.0 else symptom_match / 100.0
        r = rag_relevance if rag_relevance <= 1.0 else rag_relevance / 100.0
        w = web_val if web_val <= 1.0 else web_val / 100.0
        
        conf = (0.4 * s) + (0.4 * r) + (0.2 * w)
        return conf * 100  # Return as percentage
