"""
AVCS VIRTUAL COMPANY
Streamlit UI — Operational Decision Dashboard

FUNCTION:
- Free-form incident input
- Automatic classification
- Dynamic department processing
- Human authorization
- AVCS Record generation
"""

import sys
import os

# Добавляем корневую папку проекта в sys.path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import streamlit as st
import json
from datetime import datetime
import re

# Импорт департаментов и других компонентов
from core.departments import (
    LookoutDepartment,
    ChartsDepartment,
    GyroDepartment,
    NavigatorDepartment,
    CompassDepartment,
    HelmDepartment,
    CaptainDepartment,
)
from core.dispatcher import Dispatcher
from core.aggregation import Aggregator
from core.conflict_detection import ConflictDetector
from core.decision_engine import DecisionEngine
from core.authority_gate import AuthorityGate
from core.state_machine import StateMachine


# --- Настройка страницы ---
st.set_page_config(
    page_title="AVCS Virtual Company",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 AVCS VIRTUAL COMPANY")
st.subheader("AI-Driven Operational Decision Architecture")

# --- Инициализация сессии ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.event_id = None
    st.session_state.current_step = "input"
    st.session_state.event_data = None
    st.session_state.dispatcher_results = None
    st.session_state.department_results = None
    st.session_state.aggregated_state = None
    st.session_state.conflict_result = None
    st.session_state.decision_proposal = None
    st.session_state.authority_state = None
    st.session_state.authorized = None

# --- Sidebar ---
with st.sidebar:
    st.header("System Status")
    if st.session_state.event_id:
        st.info(f"Event: {st.session_state.event_id}")
    st.write(f"Step: {st.session_state.current_step}")
    st.divider()
    st.header("Architecture")
    st.caption("INCIDENT → DISPATCHER → 7 Dpts. → AGGREGATION → CONFLICT → DECISION → AUTHORITY → EXECUTION → RECORD")
    st.divider()
    st.caption("Version: 0.1 — MVP")

# --- Основные вкладки ---
tab1, tab2, tab3, tab4 = st.tabs(["📥 Incident Input", "⚙️ Processing", "📋 Decision", "📊 Record"])


# --- TAB 1: INCIDENT INPUT ---
with tab1:
    st.header("Incident Input")
    st.caption("Describe any incident — the system will classify and process it automatically.")

    # --- Свободное описание инцидента ---
    incident_description = st.text_area(
        "Incident Description",
        height=150,
        placeholder="Describe the incident in detail...\n\nExample: 'Hull breach in compartment 3, water ingress 50 tons/hour, vessel listing 12 degrees, position 35°N 45°W, weather storm force 5'"
    )

    # --- Дополнительные структурированные поля (опционально) ---
    col1, col2 = st.columns(2)
    with col1:
        object_type = st.text_input("Object / Vessel (optional)", placeholder="e.g., Tanker, FPSO, Plant")
        position = st.text_input("Position (optional)", placeholder="e.g., 35°N 45°W")
    with col2:
        heading = st.number_input("Heading (optional)", min_value=0, max_value=360, value=0)
        speed = st.number_input("Speed (optional)", min_value=0, max_value=100, value=0)

    # --- Кнопка обработки ---
    if st.button("🚀 Process Incident", type="primary"):
        if not incident_description.strip():
            st.error("Please describe the incident.")
        else:
            # --- Формируем данные для обработки ---
            event_data = {
                "event_id": f"EVT-{datetime.utcnow().strftime('%Y%m%d')}-001",
                "description": incident_description,
                "object": object_type if object_type else "Unknown",
                "position": position if position else "Unknown",
                "heading": heading,
                "speed": speed,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "escalate": True
            }

            st.session_state.event_data = event_data
            st.session_state.event_id = event_data["event_id"]
            st.session_state.current_step = "processing"
            st.rerun()

    if st.session_state.event_id:
        st.success(f"Event created: {st.session_state.event_id}")


# --- TAB 2: PROCESSING ---
with tab2:
    st.header("Processing Pipeline")

    if st.session_state.current_step == "processing" and st.session_state.event_data:
        with st.spinner("Processing incident..."):
            # --- Создаём департаменты ---
            lookout = LookoutDepartment()
            charts = ChartsDepartment()
            gyro = GyroDepartment()
            navigator = NavigatorDepartment()
            compass = CompassDepartment()
            helm = HelmDepartment()
            captain = CaptainDepartment()

            # --- Создаём диспетчер и регистрируем департаменты ---
            dispatcher = Dispatcher()
            dispatcher.register_department(lookout)
            dispatcher.register_department(charts)
            dispatcher.register_department(gyro)
            dispatcher.register_department(navigator)
            dispatcher.register_department(compass)
            dispatcher.register_department(helm)
            dispatcher.register_department(captain)

            # --- Создаём остальные компоненты ---
            aggregator = Aggregator()
            conflict_detector = ConflictDetector()
            decision_engine = DecisionEngine()
            authority_gate = AuthorityGate()
            state_machine = StateMachine()

            # --- Классифицируем инцидент на основе описания ---
            incident_text = st.session_state.event_data.get("description", "").lower()
            if "drone" in incident_text or "uav" in incident_text:
                incident_type = "DRONE"
            elif "hull" in incident_text or "breach" in incident_text or "water" in incident_text or "flood" in incident_text:
                incident_type = "HULL_BREACH"
            elif "fire" in incident_text or "smoke" in incident_text or "explosion" in incident_text:
                incident_type = "FIRE"
            elif "person" in incident_text or "man overboard" in incident_text or "casualty" in incident_text:
                incident_type = "MAN_OVERBOARD"
            elif "temperature" in incident_text or "pressure" in incident_text or "anomaly" in incident_text:
                incident_type = "ANOMALY"
            else:
                incident_type = "GENERAL"

            # --- Обогащаем данные для департаментов ---
            event_data = st.session_state.event_data.copy()
            event_data["classification"] = incident_type

            # --- Добавляем поля для NAVIGATOR, COMPASS, HELM, CAPTAIN ---
            event_data["situation"] = event_data.get("description", "Incident detected")
            event_data["time_to_event"] = 5  # Будет переопределено департаментами
            event_data["action"] = "Analyze and respond"
            event_data["authorized"] = False
            event_data["decision_proposal"] = "Awaiting assessment"
            event_data["evidence"] = [
                f"Incident type: {incident_type}",
                f"Description: {event_data.get('description', '')[:100]}"
            ]
            event_data["current_heading"] = event_data.get("heading", 0)
            event_data["current_speed"] = event_data.get("speed", 0)
            event_data["threat_heading"] = 0
            event_data["threat_speed"] = 0
            event_data["separation_required"] = 0.5

            # --- Запускаем обработку ---
            state_machine.start(st.session_state.event_id)

            state_machine.dispatch()
            dispatcher_results = dispatcher.process_incoming_event(event_data)

            state_machine.process()
            task_packets = dispatcher_results.get("task_packets", [])
            department_results = {}
            for packet in task_packets:
                dept_name = packet["department"]
                dept_data = packet["data"]
                if dept_name == "LOOKOUT Dpt.":
                    result = lookout.process(dept_data)
                elif dept_name == "CHARTS Dpt.":
                    result = charts.process(dept_data)
                elif dept_name == "GYRO Dpt.":
                    result = gyro.process(dept_data)
                elif dept_name == "NAVIGATOR Dpt.":
                    result = navigator.process(dept_data)
                elif dept_name == "COMPASS Dpt.":
                    result = compass.process(dept_data)
                elif dept_name == "HELM Dpt.":
                    result = helm.process(dept_data)
                elif dept_name == "CAPTAIN Dpt.":
                    result = captain.process(dept_data)
                else:
                    result = {"error": f"Unknown department: {dept_name}"}
                department_results[dept_name] = result

            state_machine.aggregate()
            aggregated_state = aggregator.aggregate(department_results, st.session_state.event_id)

            state_machine.detect_conflicts()
            conflict_result = conflict_detector.detect(aggregated_state)

            state_machine.formulate_decision()
            decision_proposal = decision_engine.formulate(aggregated_state, conflict_result)

            state_machine.wait_for_authority()
            authority_state = authority_gate.present_decision(decision_proposal)

            # --- Сохраняем результаты ---
            st.session_state.dispatcher_results = dispatcher_results
            st.session_state.department_results = department_results
            st.session_state.aggregated_state = aggregated_state
            st.session_state.conflict_result = conflict_result
            st.session_state.decision_proposal = decision_proposal
            st.session_state.authority_state = authority_state
            st.session_state.current_step = "authority"

            st.rerun()

    # --- Отображение результатов обработки ---
    if st.session_state.department_results:
        st.subheader("Department Assessments")
        for dept, result in st.session_state.department_results.items():
            with st.expander(f"📋 {dept}"):
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.json(result)

    if st.session_state.aggregated_state:
        st.subheader("📊 Aggregated State")
        st.json(st.session_state.aggregated_state)

    if st.session_state.conflict_result:
        st.subheader("⚠️ Conflict Detection")
        if st.session_state.conflict_result.get("has_conflicts"):
            st.warning("Conflicts detected!")
        else:
            st.success("No conflicts detected")
        st.json(st.session_state.conflict_result)


# --- TAB 3: DECISION ---
with tab3:
    st.header("Decision Authority")

    if st.session_state.decision_proposal:
        st.subheader("Decision Proposal")
        st.json(st.session_state.decision_proposal)

    if st.session_state.authority_state:
        st.subheader("Authority Gate")
        st.json(st.session_state.authority_state)

        if st.session_state.authority_state.get("status") == "PENDING":
            st.divider()
            st.markdown("### 🔐 Human Authorization Required")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", type="primary"):
                    st.session_state.authorized = True
                    st.session_state.current_step = "executing"
                    st.rerun()
            with col2:
                if st.button("❌ Reject", type="secondary"):
                    st.session_state.authorized = False
                    st.session_state.current_step = "completed"
                    st.rerun()

        if st.session_state.authorized is True:
            st.success("✅ Decision Authorized")
            st.session_state.current_step = "completed"
        elif st.session_state.authorized is False:
            st.error("❌ Decision Rejected")


# --- TAB 4: RECORD ---
with tab4:
    st.header("AVCS Decision Record")

    if st.session_state.current_step == "completed":
        if st.session_state.authorized:
            st.success("Decision Cycle Completed — Authorized")
        else:
            st.info("Decision Cycle Completed — Rejected")

        record = {
            "event_id": st.session_state.event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "COMPLETED",
            "authorized": st.session_state.authorized,
            "decision_proposal": st.session_state.decision_proposal,
            "authority_state": st.session_state.authority_state,
            "aggregated_state": st.session_state.aggregated_state,
            "conflict_result": st.session_state.conflict_result
        }

        st.json(record)

        st.download_button(
            label="📥 Download AVCS Record",
            data=json.dumps(record, indent=2),
            file_name=f"AVCS_RECORD_{st.session_state.event_id}.json",
            mime="application/json"
        )
    else:
        st.info("Complete the decision cycle to generate AVCS Record")
