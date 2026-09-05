"""
AVCS VIRTUAL COMPANY
AI Dispatcher — Information Routing Layer

FUNCTION:
- Receive incoming information
- Classify information type
- Determine which Departments need to process it
- Create task packets for each Department
- Route information to appropriate Departments
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


class Dispatcher:
    """
    AI Dispatcher routes incoming information to appropriate Departments.
    
    Responsibilities:
    - Classify incoming information
    - Determine relevant Departments
    - Create task packets
    - Route information
    - Maintain routing log
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.routing_log = []
        self.departments = []
        self.event_id = None

    def register_department(self, department) -> None:
        """Register a Department with the Dispatcher."""
        self.departments.append(department)
        self._log(f"Department registered: {department.department_name}")

    def process_incoming_event(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming event and route to appropriate Departments.
        
        Args:
            input_data: Dictionary containing incoming information
            
        Returns:
            Routing result with assignments and routing log
        """
        # Generate event ID
        self.event_id = f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        input_data["event_id"] = self.event_id

        self._log(f"Processing incoming event: {self.event_id}")

        # Classify the information
        classification = self._classify_information(input_data)
        self._log(f"Classification: {classification}")

        # Determine which Departments are needed
        required_departments = self._determine_required_departments(classification, input_data)
        self._log(f"Required Departments: {[d for d in required_departments]}")

        # Create task packets for each Department
        task_packets = self._create_task_packets(required_departments, input_data)

        # Route to Departments
        routing_result = self._route_to_departments(task_packets)

        # Log routing
        routing_entry = {
            "event_id": self.event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "classification": classification,
            "required_departments": [d.department_name for d in required_departments],
            "packets_count": len(task_packets),
            "routing_result": routing_result
        }
        self.routing_log.append(routing_entry)

        return {
            "event_id": self.event_id,
            "classification": classification,
            "required_departments": [d.department_name for d in required_departments],
            "task_packets": task_packets,
            "routing_result": routing_result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def _classify_information(self, input_data: Dict[str, Any]) -> str:
        """Classify the type of incoming information."""
        # Check for drone detection
        if "drone" in str(input_data).lower() or "uav" in str(input_data).lower():
            return "THREAT_DETECTION"
        # Check for anomaly
        if "anomaly" in str(input_data).lower() or "deviation" in str(input_data).lower():
            return "ANOMALY"
        # Check for environmental
        if "position" in str(input_data).lower() or "location" in str(input_data).lower():
            return "ENVIRONMENTAL"
        # Default
        return "GENERAL"

    def _determine_required_departments(self, classification: str, input_data: Dict[str, Any]) -> List:
        """Determine which Departments are needed for this event."""
        required = []
        
        # Always include LOOKOUT for any event
        lookout = self._find_department("LOOKOUT Dpt.")
        if lookout:
            required.append(lookout)

        # For threat detection, include all departments
        if classification == "THREAT_DETECTION":
            for dept in self.departments:
                if dept.department_name != "LOOKOUT Dpt.":
                    required.append(dept)
        
        # For environmental, include CHARTS and GYRO
        elif classification == "ENVIRONMENTAL":
            charts = self._find_department("CHARTS Dpt.")
            gyro = self._find_department("GYRO Dpt.")
            if charts:
                required.append(charts)
            if gyro:
                required.append(gyro)
        
        # For anomaly, include LOOKOUT, CHARTS, GYRO, NAVIGATOR
        elif classification == "ANOMALY":
            charts = self._find_department("CHARTS Dpt.")
            gyro = self._find_department("GYRO Dpt.")
            navigator = self._find_department("NAVIGATOR Dpt.")
            if charts:
                required.append(charts)
            if gyro:
                required.append(gyro)
            if navigator:
                required.append(navigator)

        # Always include CAPTAIN for decision
        captain = self._find_department("CAPTAIN Dpt.")
        if captain:
            required.append(captain)

        return required

    def _find_department(self, name: str):
        """Find a Department by name."""
        for dept in self.departments:
            if dept.department_name == name:
                return dept
        return None

    def _create_task_packets(self, departments: List, input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create task packets for each Department."""
        packets = []
        for dept in departments:
            # Prepare data based on Department type
            dept_data = input_data.copy()
            packets.append({
                "department": dept.department_name,
                "data": dept_data,
                "event_id": self.event_id,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        return packets

    def _route_to_departments(self, task_packets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Route task packets to Departments and collect results."""
        results = {}
        for packet in task_packets:
            dept_name = packet["department"]
            dept = self._find_department(dept_name)
            if dept:
                try:
                    result = dept.process(packet["data"])
                    results[dept_name] = result
                    self._log(f"Department {dept_name} processed successfully")
                except Exception as e:
                    results[dept_name] = {
                        "error": str(e),
                        "status": "FAILED"
                    }
                    self._log(f"Department {dept_name} failed: {e}", "ERROR")
            else:
                results[dept_name] = {
                    "error": "Department not found",
                    "status": "FAILED"
                }
        return results

    def _log(self, message: str, level: str = "INFO"):
        """Simple logging for Dispatcher."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] [DISPATCHER] [{level}] {message}")

    def get_routing_log(self) -> List[Dict[str, Any]]:
        """Return the routing log."""
        return self.routing_log
