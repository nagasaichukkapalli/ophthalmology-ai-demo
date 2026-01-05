from utils.scoring import Scorer

class ConfidenceAgent:
    def __init__(self):
        pass

    def calculate(self, symptom_score, rag_score, web_score):
        """
        Calculates final confidence score.
        """
        return Scorer.calculate_confidence(symptom_score, rag_score, web_score)
