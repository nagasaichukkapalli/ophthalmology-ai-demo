import os
import sys

# Ensure we can import from local directories
sys.path.append(os.getcwd())

from utils.relevance_checker import RelevanceChecker

def test_relevance():
    print("Initializing Relevance Checker...")
    checker = RelevanceChecker()
    
    test_cases = [
        ("I have blurred vision and pain", True),
        ("I want to buy some medicine", False),
        ("Hello world", False),
        ("My eyes are very red and itchy", True),
        ("Can I order contact lenses", False)
    ]
    
    print("\n--- Running Relevance Tests ---")
    for text, expected in test_cases:
        is_relevant, reason = checker.check_relevance(text)
        status = "PASS" if is_relevant == expected else "FAIL"
        print(f"Input: '{text}' | Expected: {expected} | Actual: {is_relevant} | Reason: {reason} -> {status}")

if __name__ == "__main__":
    test_relevance()
