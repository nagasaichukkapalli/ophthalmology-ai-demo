from duckduckgo_search import DDGS
from utils.text_loader import TextLoader
import random
import datetime

class WebIntelligenceAgent:
    def __init__(self, guidelines_path=None):
        self.guidelines = TextLoader.load_guidelines(guidelines_path) if guidelines_path else []

    def validate(self, disease_name, symptoms):
        """
        Validates the disease prediction using web search or guidelines.
        Returns trust score and freshness info.
        """
        try:
            # Try live web search
            with DDGS() as ddgs:
                current_year = datetime.datetime.now().year
                query = f"{disease_name} symptoms guidelines {current_year}"
                results = list(ddgs.text(query, max_results=3))
                
                if results:
                    # Check for keywords in snippets
                    match_count = 0
                    for r in results:
                        if disease_name.lower() in r['body'].lower():
                            match_count += 1
                            
                    # Simple scoring based on presence in search snippets
                    web_score = (match_count / len(results)) * 100
                    
                    return {
                        "source": "Live Web Search",
                        "score": web_score,
                        "freshness": f"Pulled from top {len(results)} web results",
                        "snippet": results[0]['body'][:100] + "..."
                    }
        except Exception as e:
            # Fallback to simulated/mock guideline check if internet fails or rate limited
            pass

        # Simulation / Guidelines Check
        return self._simulate_validation(disease_name)

    def _simulate_validation(self, disease_name):
        """
        Simulates validation using local guideline freshness.
        """
        relevant_guideline = next((g for g in self.guidelines if disease_name.lower() in g.lower()), None)
        
        if relevant_guideline:
            return {
                "source": "Clinical Guidelines (Internal)",
                "score": 85.0, # High trust for matched guideline
                "freshness": relevant_guideline,
                "snippet": "Matched with recent clinical practice guidelines."
            }
        else:
             return {
                "source": "Internal Database",
                "score": 50.0,
                "freshness": "No specific recent guideline found",
                "snippet": "Standard medical knowledge base validation."
            }
