"""
AVCS VIRTUAL COMPANY
Semantic Analyzer

Version: v0.3.2 — Semantic Window
"""

import re
from typing import Dict, Any, List, Optional


class SemanticAnalyzer:
    """
    Semantic Analyzer processes raw text to extract structured meaning.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        print("🔥🔥🔥 AVCS SEMANTIC ANALYZER v0.3.2 LOADED")

    def analyze(self, text: str, keyword: str) -> Dict[str, Any]:
        print("🔥🔥🔥 AVCS ANALYZE v0.3.2")
        print(f"TEXT = {text[:200]}...")
        print(f"KEYWORD = {keyword}")

        # Negation patterns
        NEGATION_PATTERNS = [
            r"\bno\s+",
            r"\bnot\s+",
            r"\bwithout\s+",
            r"\bnever\s+",
            r"\bruled\s+out\s*",
            r"\bexcluded\s*",
            r"\babsent\s*",
            r"\bnot\s+detected\s*",
            r"\bno\s+evidence\s*",
        ]

        UNCERTAINTY_PATTERNS = [
            r"\bpossible\s+",
            r"\bsuspected\s+",
            r"\bprobable\s+",
            r"\bprobably\s+",
            r"\bmaybe\s+",
            r"\bpotential\s+",
            r"\bappears?\s*",
            r"\bseems?\s*",
            r"\bindicates?\s*",
            r"\bsuggests?\s*",
        ]

        CONTEXT_PATTERNS = {
            "previous": [r"\bprevious\s+", r"\bprior\s+", r"\bhistorical\s+", r"\bearlier\s+"],
            "reported": [r"\breported\s+", r"\bstated\s+", r"\baccording to\s+"],
            "current": [r"\bcurrent\s+", r"\bnow\s+", r"\bat this time\s+"],
            "confirmed": [r"\bconfirmed\s+", r"\bverified\s+", r"\bvalidated\s+"],
        }

        keyword_pos = text.lower().find(keyword.lower())
        if keyword_pos == -1:
            return {
                "detected": False,
                "polarity": "NEUTRAL",
                "uncertainty": None,
                "context": None,
                "confidence": 0.0,
                "negation_found": False,
                "uncertainty_found": False
            }

        # --- SEMANTIC WINDOW ---
        window_start = max(0, keyword_pos - 50)
        window_end = min(len(text), keyword_pos + len(keyword) + 50)
        window_text = text[window_start:window_end]
        print(f"🔥🔥🔥 SEMANTIC WINDOW = [{window_text}]")

        # --- CHECK NEGATION ---
        negation_found = False
        for pattern in NEGATION_PATTERNS:
            if re.search(pattern, window_text):
                negation_found = True
                break

        # --- CHECK UNCERTAINTY ---
        uncertainty_found = False
        for pattern in UNCERTAINTY_PATTERNS:
            if re.search(pattern, window_text):
                uncertainty_found = True
                break

        # --- CHECK CONTEXT ---
        context_type = None
        for ctx_type, patterns in CONTEXT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, window_text):
                    context_type = ctx_type.upper()
                    break
            if context_type:
                break

        # --- DETERMINE POLARITY ---
        if negation_found:
            polarity = "NEGATIVE"
        elif uncertainty_found:
            polarity = "NEUTRAL"
        else:
            polarity = "POSITIVE"

        # --- DETERMINE CONFIDENCE ---
        confidence = 0.8
        if negation_found:
            confidence = 0.95
        elif uncertainty_found:
            confidence = 0.6
        if context_type == "REPORTED":
            confidence = 0.7
        if context_type == "CONFIRMED":
            confidence = 0.95

        result = {
            "detected": True,
            "polarity": polarity,
            "uncertainty": "HIGH" if uncertainty_found else None,
            "context": context_type,
            "confidence": confidence,
            "negation_found": negation_found,
            "uncertainty_found": uncertainty_found,
            "context_text": window_text.strip()
        }

        print(f"🔥🔥🔥 RESULT: {result}")
        return result
