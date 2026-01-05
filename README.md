# Ophthalmology AI Clinical Decision Support (Demo)

**A Confidence-Guided Multi-Agent Framework for Ophthalmology Clinical Decision Support Using Biomedical RAG and Web Intelligence**

> **⚠️ ACADEMIC DEMONSTRATION ONLY**
>
> This system is NOT a medical device. It does not provide diagnosis or treatment advice. 
> All outputs are informational and must be verified by a qualified specialist.

## Overview

This project demonstrates a multi-agent AI system that:
1.  **Analyzes Symptoms**: Extracts key clinical terms from patient descriptions.
2.  **Retrieves Knowledge**: Matches symptoms to a curated eye disease database using RAG (Retrieval-Augmented Generation).
3.  **Validates Findings**: Checks disease consistency against clinical guidelines using simulated or live web intelligence.
4.  **Calculates Confidence**: Provides a transparent confidence score to guide decision-making.

## Architecture

-   **SymptomAnalysisAgent**: Rule-based extraction of symptoms and severity estimation.
-   **DiseaseRetrievalAgent**: RAG implementation using `sentence-transformers` (all-MiniLM-L6-v2) and `faiss-cpu`.
-   **WebIntelligenceAgent**: Validates candidates against `data/guidelines.txt` or via DuckDuckGo search.
-   **DecisionAgent**: Aggregates all signals into a final recommendation.
-   **ConfidenceAgent**: Computes a weighted confidence score (40% Symptom, 40% RAG, 20% Web).

## Installation

1.  **Clone resources** (if applicable) or ensure you have the file structure.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

## Structure

```
ophthalmology-ai-demo/
│
├── app.py                      # Main UI
├── agents/                     # AI Agents (Modular Logic)
│   ├── symptom_agent.py
│   ├── rag_agent.py
│   ├── ...
├── data/                       # Knowledge Base
│   ├── eye_diseases.txt
│   └── guidelines.txt
├── embeddings/                 # FAISS Index Storage
└── utils/                      # Helper Modules
```

## System Logic (Confidence Calculation)

The system calculates confidence as:
`Confidence = (0.4 * SymptomMatch) + (0.4 * RAGSimilarity) + (0.2 * WebValidation)`

If `Confidence < 60%`, the system automatically flags a "Low Confidence" warning.


