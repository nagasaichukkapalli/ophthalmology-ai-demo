from agents.confidence_agent import ConfidenceAgent

class DecisionAgent:
    def __init__(self):
        self.confidence_agent = ConfidenceAgent()

    def decide(self, symptom_data, rag_results, web_result):
        """
        Combines all agent outputs to make a recommendation.
        """
        # Default if no RAG results
        if not rag_results:
            return {
                "disease": "Unknown",
                "specialist": "General Ophthalmologist",
                "explanation": "No matching disease found in database.",
                "confidence": 0,
                "warning": True
            }

        top_match = rag_results[0]
        disease = top_match['disease']
        rag_score = top_match['score']
        
        # Calculate symptom overlap score (simple heuristic)
        # Check how many extracted symptoms are in the disease symptom list
        disease_symptoms_list = [s.strip().lower() for s in disease['symptoms'].split(',')]
        user_symptoms = symptom_data['symptoms']
        
        match_count = sum(1 for s in user_symptoms if any(ds in s or s in ds for ds in disease_symptoms_list))
        total_extracted = len(user_symptoms) if user_symptoms else 1
        symptom_score = (match_count / total_extracted) * 100
        
        # Web score
        web_score = web_result['score']
        
        # Final Confidence
        confidence = self.confidence_agent.calculate(symptom_score, rag_score, web_score)
        
        explanation = (
            f"Based on your symptoms ({', '.join(user_symptoms)}), "
            f"the system identified {disease['name']} as a potential match "
            f"(RAG Similarity: {rag_score:.1f}%). "
            f"External validation via {web_result['source']} returned a trust score of {web_score:.1f}%."
        )
        
        return {
            "disease": disease['name'],
            "specialist": disease['specialist'],
            "explanation": explanation,
            "confidence": confidence,
            "warning": confidence < 60
        }
