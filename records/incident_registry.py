"""
AVCS VIRTUAL COMPANY
Incident Registry — History Storage

FUNCTION:
- Store incident records
- Retrieve incident history
- Filter by type, severity, status
- Update incident status (e.g., after authorization)
- Clear old records
"""

import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
import uuid


class IncidentRegistry:
    """
    Incident Registry stores and manages incident records.
    """

    def __init__(self, data_file: str = "data/incident_registry.json"):
        self.data_file = data_file
        self._ensure_data_file()

    def _ensure_data_file(self):
        """Ensure the data file exists."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as f:
                json.dump([], f)

    def _load_data(self) -> List[Dict[str, Any]]:
        """Load all records from the data file."""
        with open(self.data_file, "r") as f:
            return json.load(f)

    def _save_data(self, data: List[Dict[str, Any]]):
        """Save records to the data file."""
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def generate_event_id(self) -> str:
        """Generate a unique event ID."""
        return f"EVT-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    def add_incident(self, incident_data: Dict[str, Any]) -> str:
        """Add a new incident record."""
        data = self._load_data()
        
        # Ensure event_id exists
        if "event_id" not in incident_data:
            incident_data["event_id"] = self.generate_event_id()
        
        # Add timestamp if not present
        if "timestamp" not in incident_data:
            incident_data["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Set default status if not present
        if "status" not in incident_data:
            incident_data["status"] = "RECEIVED"
        
        data.append(incident_data)
        self._save_data(data)
        return incident_data["event_id"]

    def update_incident(self, event_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing incident record by event_id.
        
        Args:
            event_id: The ID of the incident to update.
            updates: Dictionary of fields to update.
            
        Returns:
            True if updated, False if not found.
        """
        data = self._load_data()
        
        for incident in data:
            if incident.get("event_id") == event_id:
                incident.update(updates)
                incident["updated_at"] = datetime.now(timezone.utc).isoformat()
                self._save_data(data)
                return True
        
        return False

    def get_incident(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific incident by event_id."""
        data = self._load_data()
        for incident in data:
            if incident.get("event_id") == event_id:
                return incident
        return None

    def get_all_incidents(self) -> List[Dict[str, Any]]:
        """Get all incidents."""
        return self._load_data()

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about incidents."""
        data = self._load_data()
        
        stats = {
            "total": len(data),
            "by_type": {},
            "by_severity": {},
            "by_status": {},
        }
        
        for incident in data:
            event_type = incident.get("event_type", "UNKNOWN")
            severity = incident.get("severity", "UNKNOWN")
            status = incident.get("status", "UNKNOWN")
            
            stats["by_type"][event_type] = stats["by_type"].get(event_type, 0) + 1
            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        return stats

    def clear_old_records(self, days: int = 30) -> int:
        """Clear records older than specified days."""
        data = self._load_data()
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        
        new_data = []
        removed_count = 0
        
        for incident in data:
            timestamp = incident.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if dt > cutoff:
                        new_data.append(incident)
                    else:
                        removed_count += 1
                except:
                    new_data.append(incident)
            else:
                new_data.append(incident)
        
        self._save_data(new_data)
        return removed_count

    def clear_all(self) -> int:
        """Clear all records."""
        data = self._load_data()
        count = len(data)
        self._save_data([])
        return count
