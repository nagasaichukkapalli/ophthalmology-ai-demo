import os
import sys

# Ensure we can import from local directories
sys.path.append(os.getcwd())

from agents.symptom_agent import SymptomAnalysisAgent
from agents.rag_agent import DiseaseRetrievalAgent
from agents.web_agent import WebIntelligenceAgent
from agents.decision_agent import DecisionAgent

def test_system():
    print("Initializing Agents...")
    data_path = os.path.join("data", "eye_diseases.txt")
    guide_path = os.path.join("data", "guidelines.txt")
    
    # Check files exist
    if not os.path.exists(data_path):
        print(f"ERROR: {data_path} not found")
        return
    if not os.path.exists(guide_path):
        print(f"ERROR: {guide_path} not found")
        return

    try:
        symptom_agent = SymptomAnalysisAgent()
        rag_agent = DiseaseRetrievalAgent(data_path, "embeddings")
        web_agent = WebIntelligenceAgent(guide_path)
        decision_agent = DecisionAgent()
        print("Agents Initialized Successfully.")
    except Exception as e:
        print(f"ERROR initializing agents: {e}")
        return

    # Test Case
    test_input = "I have severe redness, itching, and a gritty sensation in my right eye with discharge."
    print(f"\n--- Test Input: '{test_input}' ---\n")

    # 1. Symptom Analysis
    print("1. Running Symptom Analysis...")
    symptom_data = symptom_agent.analyze(test_input)
    print(f"   Detected Symptoms: {symptom_data['symptoms']}")
    print(f"   Severity: {symptom_data['severity']}")

    # 2. RAG Retrieval
    print("2. Running RAG Retrieval...")
    rag_results = rag_agent.retrieve(test_input)
    if rag_results:
        top = rag_results[0]
        print(f"   Top Match: {top['disease']['name']} (Score: {top['score']:.2f})")
    else:
        print("   No RAG results found.")

    # 3. Web Validation
    print("3. Running Web Validation...")
    disease_name = rag_results[0]['disease']['name'] if rag_results else "Unknown"
    web_result = web_agent.validate(disease_name, symptom_data['symptoms'])
    print(f"   Source: {web_result['source']}")
    print(f"   Score: {web_result['score']}")

    # 4. Decision
    print("4. Making Decision...")
    decision = decision_agent.decide(symptom_data, rag_results, web_result)
    
    print("\n--- Final Output ---")
    print(f"Disease: {decision['disease']}")
    print(f"Specialist: {decision['specialist']}")
    print(f"Confidence: {decision['confidence']:.2f}%")
    print(f"Warning Triggered: {decision['warning']}")
    print(f"Explanation: {decision['explanation']}")

if __name__ == "__main__":
    test_system()
