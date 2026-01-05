import streamlit as st
import os

# Set page config FIRST
st.set_page_config(page_title="OphthalmoAI Demo", layout="wide")

# Imports after page config
from agents.symptom_agent import SymptomAnalysisAgent
from agents.rag_agent import DiseaseRetrievalAgent
from agents.web_agent import WebIntelligenceAgent
from agents.decision_agent import DecisionAgent

# Initialize Agents
@st.cache_resource
def load_agents():
    data_path = os.path.join("data", "eye_diseases.txt")
    guide_path = os.path.join("data", "guidelines.txt")
    return {
        "symptom": SymptomAnalysisAgent(),
        "rag": DiseaseRetrievalAgent(data_path, "embeddings"),
        "web": WebIntelligenceAgent(guide_path),
        "decision": DecisionAgent()
    }

agents = load_agents()

# Sidebar
st.sidebar.title("System Architecture")
st.sidebar.info(
    """
    **Multi-Agent Design:**
    - 🗣️ **Symptom Agent**: Extracts clinical terms
    - 🔍 **RAG Agent**: Finds disease matches
    - 🌐 **Web Agent**: Validates with guidelines
    - 🧠 **Decision Agent**: Synthesizes output
    """
)
st.sidebar.warning("⚠️ For Academic Demonstration Only")

# Main UI
st.title("👁️ Ophthalmology Clinical Decision Support (Demo)")
st.markdown(
    """
    > **DISCLAIMER:** This system is for **academic demonstration purposes only**. 
    > It is **NOT** a medical device. It does **NOT** provide diagnosis. 
    > Consult a qualified specialist for any eye health concerns.
    """
)

# Input
symptom_text = st.text_area("Describe your eye symptoms:", height=100, placeholder="e.g., I have redness and gritty sensation in my right eye...")

if st.button("Analyze Symptoms"):
    if not symptom_text:
        st.error("Please enter symptoms to analyze.")
    else:
        with st.spinner("Multi-Agent System Analyzing..."):
            # 1. Symptom Extraction
            st.text("Agent 1: Extracting symptoms...")
            symptom_data = agents["symptom"].analyze(symptom_text)
            
            # 2. Retrieval
            st.text("Agent 2: Retrieving disease knowledge...")
            rag_results = agents["rag"].retrieve(symptom_data["original_text"])
            top_disease_name = rag_results[0]['disease']['name'] if rag_results else "Unknown"
            
            # 3. Web Validation
            st.text("Agent 3: Validating against guidelines...")
            web_result = agents["web"].validate(top_disease_name, symptom_data["symptoms"])
            
            # 4. Decision
            st.text("Agent 4: Computing final decision...")
            decision = agents["decision"].decide(symptom_data, rag_results, web_result)
            
        # Display Results
        st.divider()
        st.subheader("Analysis Results")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 🩺 Probable Condition: **{decision['disease']}**")
            st.markdown(f"**Recommended Specialist:** {decision['specialist']}")
            st.info(f"**Reasoning:** {decision['explanation']}")
            
            if decision['warning']:
                st.error("⚠️ **Low Confidence** (< 60%) - Strong recommendation for specialist consultation.")
                
        with col2:
            st.metric("Confidence Score", f"{decision['confidence']:.1f}%")
            st.progress(min(int(decision['confidence']), 100))
            
            st.markdown("#### Evidence Sources")
            st.caption(f"**RAG Match:** {rag_results[0]['score']:.1f}% (Internal DB)")
            st.caption(f"**Validation:** {web_result['score']:.1f}% ({web_result['source']})")
