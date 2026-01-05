from sentence_transformers import SentenceTransformer, util
import numpy as np

class RelevanceChecker:
    def __init__(self):
        # Mandatory Keyword Lists
        self.eye_keywords = [
            "eye", "vision", "blurred", "pain", "redness", "discharge", "itching",
            "dryness", "light sensitivity", "floaters", "halos", "night vision"
        ]
        
        self.non_medical_keywords = [
            "buy", "purchase", "shop", "order", "price", "product", "sell", "booking", "phone"
        ]
        
        # Load same model as RAG for semantic check
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            # Reference embedding for "General Eye Symptoms"
            self.reference_text = "eye pain redness blurred vision itching discharge dry eyes light sensitivity"
            self.ref_embedding = self.model.encode(self.reference_text, convert_to_tensor=True)
        except Exception as e:
            print(f"Warning: Semantic checker failed to load model: {e}")
            self.model = None

    def check_relevance(self, text):
        """
        Runs 3 checks:
        1. Keyword Presence (Must match at least one)
        2. Intent Check (Must NOT match forbidden words)
        3. Semantic Check (Cosine similarity > 0.3)
        """
        text_lower = text.lower()
        
        # 1. Keyword Check
        has_keyword = any(k in text_lower for k in self.eye_keywords)
        if not has_keyword:
            return False, "No eye-related keywords found."

        # 2. Medical Intent Check
        has_bad_intent = any(k in text_lower for k in self.non_medical_keywords)
        if has_bad_intent:
            return False, "Input detected as non-medical (commercial/spam)."

        # 3. Semantic Similarity Check
        if self.model:
            user_embedding = self.model.encode(text, convert_to_tensor=True)
            similarity = util.cos_sim(user_embedding, self.ref_embedding).item()
            
            if similarity < 0.30:
                return False, f"Semantic Relevance too low ({similarity:.2f})."
        
        return True, "Passed"
