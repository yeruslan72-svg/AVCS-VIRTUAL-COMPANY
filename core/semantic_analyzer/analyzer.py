"""
AVCS VIRTUAL COMPANY
Semantic Analyzer

Detects:
- Polarity (positive, negative, neutral)
- Negation (no, not, without, never)
- Uncertainty (possible, suspected, maybe)
- Context (previous, historical, reported)
- Confidence (high, medium, low)
"""

import re
from typing import Dict, Any, List, Optional


class SemanticAnalyzer:
    """
    Semantic Analyzer processes raw text to extract structured meaning.
    
    Responsibilities:
    - Detect negation patterns
    - Classify polarity
    - Identify uncertainty markers
    - Determine source and context
    - Assign confidence
    """

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

    # Uncertainty markers
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

    # Context markers
    CONTEXT_PATTERNS = {
        "previous": [r"\bprevious\s+", r"\bprior\s+", r"\bhistorical\s+", r"\bearlier\s+"],
        "reported": [r"\breported\s+", r"\bstated\s+", r"\baccording to\s+"],
        "current": [r"\bcurrent\s+", r"\bnow\s+", r"\bat this time\s+"],
        "confirmed": [r"\bconfirmed\s+", r"\bverified\s+", r"\bvalidated\s+"],
    }

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def analyze(self, text: str, keyword: str) -> Dict[str, Any]:
        """
        Analyze text for a specific keyword.
        
        Returns:
            {
                "detected": bool,
                "polarity": "POSITIVE" | "NEGATIVE" | "NEUTRAL",
                "uncertainty": "HIGH" | "MEDIUM" | "LOW" | None,
                "context": "PREVIOUS" | "CURRENT" | "REPORTED" | "CONFIRMED" | None,
                "confidence": 0.0 - 1.0,
                "negation_found": bool,
                "uncertainty_found": bool
            }
        """
        # Find the keyword position
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

        # Extract context around keyword (50 chars before, 50 after)
        start = max(0, keyword_pos - 50)
        end = min(len(text), keyword_pos + 50)
        context = text[start:end]

        # Check for negation BEFORE the keyword
        negation_found = False
        for pattern in self.NEGATION_PATTERNS:
            if re.search(pattern, text[max(0, keyword_pos - 30):keyword_pos]):
                negation_found = True
                break

        # Check for uncertainty BEFORE the keyword
        uncertainty_found = False
        for pattern in self.UNCERTAINTY_PATTERNS:
            if re.search(pattern, text[max(0, keyword_pos - 30):keyword_pos]):
                uncertainty_found = True
                break

        # Determine polarity
        if negation_found:
            polarity = "NEGATIVE"
        elif uncertainty_found:
            polarity = "NEUTRAL"
        else:
            polarity = "POSITIVE"

        # Determine context
        context_type = None
        for ctx_type, patterns in self.CONTEXT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text[max(0, keyword_pos - 50):keyword_pos]):
                    context_type = ctx_type.upper()
                    break
            if context_type:
                break

        # Determine confidence
        confidence = 0.8  # Default
        if negation_found:
            confidence = 0.95
        elif uncertainty_found:
            confidence = 0.6
        if context_type == "REPORTED":
            confidence = 0.7
        if context_type == "CONFIRMED":
            confidence = 0.95

        return {
            "detected": True,
            "polarity": polarity,
            "uncertainty": "HIGH" if uncertainty_found else None,
            "context": context_type,
            "confidence": confidence,
            "negation_found": negation_found,
            "uncertainty_found": uncertainty_found,
            "context_text": context
        }
