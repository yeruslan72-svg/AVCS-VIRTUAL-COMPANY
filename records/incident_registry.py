"""
AVCS VIRTUAL COMPANY
Incident Registry — Хранилище всех инцидентов

FUNCTION:
- Сохранять все обработанные инциденты
- Присваивать уникальные ID
- Автоматически удалять записи старше 30 дней
- Просматривать историю
- Получать статистику
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


class IncidentRegistry:
    """
    Incident Registry хранит историю всех инцидентов.
    """

    def __init__(self, storage_path: str = "data/incidents.json", retention_days: int = 30):
        self.storage_path = storage_path
        self.retention_days = retention_days
        self.incidents = []
        self._counter = 1
        self._load()
        self._clean_old_records()

    def _load(self):
        """Загрузить инциденты из файла."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.incidents = data.get("incidents", [])
                    self._counter = data.get("counter", len(self.incidents) + 1)
                print(f"[INCIDENT_REGISTRY] Loaded {len(self.incidents)} incidents, counter: {self._counter}")
            except Exception as e:
                print(f"[INCIDENT_REGISTRY] Error loading: {e}")
                self.incidents = []
                self._counter = 1
        else:
            print(f"[INCIDENT_REGISTRY] No existing file, starting fresh")
            self._counter = 1

    def _save(self):
        """Сохранить инциденты в файл."""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "incidents": self.incidents,
                    "counter": self._counter
                }, f, indent=2, ensure_ascii=False)
            print(f"[INCIDENT_REGISTRY] Saved {len(self.incidents)} incidents to {self.storage_path}")
        except Exception as e:
            print(f"[INCIDENT_REGISTRY] ERROR saving: {e}")

    def _clean_old_records(self):
        """Удалить записи старше retention_days."""
        if not self.incidents:
            return
        
        now = datetime.utcnow()
        cutoff = now - timedelta(days=self.retention_days)
        original_count = len(self.incidents)
        
        cleaned_incidents = []
        for incident in self.incidents:
            try:
                timestamp_str = incident.get("timestamp", "").replace("Z", "+00:00")
                if not timestamp_str:
                    continue
                incident_time = datetime.fromisoformat(timestamp_str)
                if incident_time > cutoff:
                    cleaned_incidents.append(incident)
            except (ValueError, TypeError):
                continue
        
        self.incidents = cleaned_incidents
        
        removed = original_count - len(self.incidents)
        if removed > 0:
            print(f"[INCIDENT_REGISTRY] Removed {removed} old records (>{self.retention_days} days)")
            self._save()

    def generate_event_id(self) -> str:
        """Сгенерировать уникальный Event ID."""
        event_id = f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-{self._counter:03d}"
        self._counter += 1
        self._save()
        print(f"[INCIDENT_REGISTRY] Generated event ID: {event_id}")
        return event_id

    def add_incident(self, incident_data: Dict[str, Any]) -> str:
        """Добавить новый инцидент в реестр."""
        event_id = incident_data.get("event_id") or self.generate_event_id()
        print(f"[INCIDENT_REGISTRY] Adding incident: {event_id}")
        
        incident = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "description": incident_data.get("description", ""),
            "event_type": incident_data.get("event_type", "UNKNOWN"),
            "severity": incident_data.get("severity", "UNKNOWN"),
            "critical_conditions": incident_data.get("critical_conditions", []),
            "risk_assessment": incident_data.get("risk_assessment", {}),
            "decision_proposal": incident_data.get("decision_proposal", {}),
            "authorized": incident_data.get("authorized", False),
            "status": incident_data.get("status", "COMPLETED"),
            "record": incident_data.get("record", {})
        }
        
        self.incidents.append(incident)
        self._save()
        print(f"[INCIDENT_REGISTRY] Total incidents: {len(self.incidents)}")
        return event_id

    def get_all_incidents(self) -> List[Dict[str, Any]]:
        """Получить все инциденты."""
        print(f"[INCIDENT_REGISTRY] Returning {len(self.incidents)} incidents")
        return self.incidents

    def get_incident(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Получить инцидент по ID."""
        for incident in self.incidents:
            if incident.get("event_id") == event_id:
                return incident
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику по инцидентам."""
        total = len(self.incidents)
        by_type = {}
        by_severity = {}
        by_status = {}

        for incident in self.incidents:
            event_type = incident.get("event_type", "UNKNOWN")
            severity = incident.get("severity", "UNKNOWN")
            status = incident.get("status", "UNKNOWN")

            by_type[event_type] = by_type.get(event_type, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "total": total,
            "by_type": by_type,
            "by_severity": by_severity,
            "by_status": by_status
        }

    def get_next_event_id(self) -> str:
        """Получить следующий доступный Event ID."""
        return f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-{self._counter:03d}"

    def clear_old_records(self, days: int = None) -> int:
        """Принудительная очистка записей старше указанного количества дней."""
        if days is None:
            days = self.retention_days
        
        now = datetime.utcnow()
        cutoff = now - timedelta(days=days)
        original_count = len(self.incidents)
        
        cleaned_incidents = []
        for incident in self.incidents:
            try:
                timestamp_str = incident.get("timestamp", "").replace("Z", "+00:00")
                if not timestamp_str:
                    continue
                incident_time = datetime.fromisoformat(timestamp_str)
                if incident_time > cutoff:
                    cleaned_incidents.append(incident)
            except (ValueError, TypeError):
                continue
        
        self.incidents = cleaned_incidents
        
        removed = original_count - len(self.incidents)
        self._save()
        return removed

    def clear_all(self) -> int:
        """Очистить все записи."""
        count = len(self.incidents)
        self.incidents = []
        self._save()
        print(f"[INCIDENT_REGISTRY] Cleared all {count} records")
        return count
