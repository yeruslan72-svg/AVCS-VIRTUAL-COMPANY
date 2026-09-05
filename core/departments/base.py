"""
AVCS VIRTUAL COMPANY
Base Department Class

All Departments inherit from this class.
It enforces the standard contract structure.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import uuid


class BaseDepartment(ABC):
    """
    Base class for all AVCS Departments.
    
    Each Department has:
    - A defined purpose
    - Defined inputs
    - A constrained processing responsibility
    - Defined outputs
    - Explicit authority boundaries
    - Mandatory actions
    - Permitted recommendations
    - Prohibited decisions
    """

    def __init__(
        self,
        department_name: str,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a Department.
        
        Args:
            department_name: Name of the Department (e.g., "LOOKOUT Dpt.")
            config: Optional configuration dictionary
        """
        self.department_name = department_name
        self.config = config or {}
        self.authority_state = "NO_AUTHORITY"
        self.event_id = None

    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming data and return a structured assessment.
        
        Args:
            input_data: Dictionary containing incoming information
            
        Returns:
            Structured dictionary with assessment, evidence, recommendations
        """
        pass

    def _create_response(
        self,
        assessment: str,
        evidence: List[str],
        confidence: Optional[float] = None,
        uncertainty: Optional[List[str]] = None,
        constraints: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None,
        status: str = "COMPLETED",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a standardized response dictionary.
        
        This ensures all Departments return data in the same format.
        """
        return {
            "department": self.department_name,
            "event_id": self.event_id or kwargs.get("event_id", "UNKNOWN"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "assessment": assessment,
            "evidence": evidence or [],
            "confidence": confidence,
            "uncertainty": uncertainty or [],
            "constraints": constraints or [],
            "recommendations": recommendations or [],
            "authority_state": self.authority_state,
            "status": status,
            **kwargs
        }

    def _validate_input(self, input_data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        Validate that required fields are present in input_data.
        
        Args:
            input_data: Dictionary to validate
            required_fields: List of required field names
            
        Returns:
            True if all required fields are present, False otherwise
        """
        for field in required_fields:
            if field not in input_data or input_data[field] is None:
                return False
        return True

    def _generate_event_id(self) -> str:
        """Generate a unique event ID."""
        return f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    def _log(self, message: str, level: str = "INFO"):
        """
        Simple logging for Departments.
        
        Args:
            message: Log message
            level: Log level (INFO, WARNING, ERROR)
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [{self.department_name}] [{level}] {message}")

    def get_contract(self) -> Dict[str, Any]:
        """
        Return the Department contract.
        
        This method should be overridden by each Department.
        """
        return {
            "department": self.department_name,
            "purpose": "Not defined",
            "authority": self.authority_state,
            "prohibited_decisions": [],
            "permitted_recommendations": []
        }
