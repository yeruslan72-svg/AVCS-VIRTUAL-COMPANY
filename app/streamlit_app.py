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

# --- НОВЫЕ ИМПОРТЫ ДЛЯ v0.2 ---
from core.event_normalizer import EventNormalizer
from core.risk_engine import RiskEngine


# --- Настройка страницы ---
st.set_page_config(
    page_title="AVCS Virtual Company",
    page_icon="🧭",
    layout="wide"
)

# --- ПРИВЕТСТВЕННАЯ СТРАНИЦА (МИЛИТАРИ-СТИЛЬ) ---
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    st.markdown("""
    <style>
        .welcome-container {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 60px 40px;
            border-radius: 15px;
            border: 2px solid #c9a84c;
            box-shadow: 0 0 40px rgba(201, 168, 76, 0.2);
            text-align: center;
            margin-top: 40px;
        }
        .welcome-title {
            font-size: 48px;
            font-weight: 700;
            color: #c9a84c;
            text-shadow: 0 0 30px rgba(201, 168, 76, 0.3);
            letter-spacing: 4px;
            text-transform: uppercase;
            font-family: 'Courier New', monospace;
        }
        .welcome-subtitle {
            font-size: 20px;
            color: #8a8a8a;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            letter-spacing: 2px;
        }
        .welcome-divider {
            border: 1px solid #c9a84c;
            margin: 30px auto;
            width: 60%;
            opacity: 0.3;
        }
        .welcome-text {
            color: #c0c0c0;
            font-size: 16px;
            line-height: 1.8;
            font-family: 'Courier New', monospace;
            max-width: 700px;
            margin: 0 auto 30px auto;
        }
        .welcome-status {
            display: inline-block;
            background: #1a3a2a;
            color: #00ff88;
            padding: 8px 24px;
            border-radius: 20px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            border: 1px solid #00ff88;
            letter-spacing: 1px;
            margin-bottom: 20px;
        }
        .welcome-button {
            background: transparent;
            color: #c9a84c;
            border: 2px solid #c9a84c;
            padding: 12px 40px;
            border-radius: 5px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Courier New', monospace;
        }
        .welcome-button:hover {
            background: #c9a84c;
            color: #1a1a2e;
        }
        .welcome-version {
            color: #555;
            font-size: 12px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
        }
        .welcome-badge {
            display: inline-block;
            background: rgba(201, 168, 76, 0.1);
            border: 1px solid #c9a84c;
            color: #c9a84c;
            padding: 4px 16px;
            border-radius: 4px;
            font-size: 12px;
            letter-spacing: 1px;
            font-family: 'Courier New', monospace;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-badge">AVCS — STRUCTURAL INTEGRITY SYSTEM</div>
        <div style="height: 20px;"></div>
        <div class="welcome-title">🧭 OPERATIONAL<br>DECISION ARCHITECTURE</div>
        <div class="welcome-subtitle">AI-Driven Incident Management System</div>
        <hr class="welcome-divider">
        <div class="welcome-status">● SYSTEM READY — AWAITING COMMAND</div>
        <div class="welcome-text">
            <strong style="color: #c9a84c;">AVCS VIRTUAL COMPANY</strong> is an operational decision architecture<br>
            designed for high-risk environments.<br><br>
            <span style="color: #666;">INCIDENT → DISPATCHER → 7 Dpts. → AGGREGATION → CONFLICT → DECISION → AUTHORITY → EXECUTION → RECORD</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- КНОПКА ВХОДА ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▸ ENTER COMMAND CENTER", use_container_width=True, type="primary"):
            st.session_state.welcome_shown = True
            st.rerun()
    
    st.stop()

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---

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
    # --- Логотип AVCS ---
    try:
        st.image("app/logo.png", width=200)
    except:
        st.markdown("### 🧭 AVCS")
    
    st.divider()
    
    st.header("System Status")
    if st.session_state.get("event_id"):
        st.info(f"Event: {st.session_state.event_id}")
    else:
        st.info("No active event")
    st.write(f"Step: {st.session_state.current_step}")
    st.divider()
    st.header("Architecture")
    st.caption("INCIDENT → DISPATCHER → 7 Dpts. → AGGREGATION → CONFLICT → DECISION → AUTHORITY → EXECUTION → RECORD")
    st.divider()
    st.caption("Version: 0.2 — Information Integrity Layer")

    # --- Кнопка сброса события ---
    st.divider()
    if st.button("🔄 Reset Event", use_container_width=True):
        for key in ["event_id", "event_data", "dispatcher_results", "department_results", 
                    "aggregated_state", "conflict_result", "decision_proposal", 
                    "authority_state", "authorized", "current_step"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_step = "input"
        st.rerun()

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

            # --- НОРМАЛИЗАЦИЯ СОБЫТИЯ (v0.2) ---
            normalizer = EventNormalizer()
            normalized_data = normalizer.normalize(event_data)
            event_data = normalized_data

            st.session_state.event_data = event_data
            st.session_state.event_id = event_data["event_id"]
            st.session_state.current_step = "processing"
            st.rerun()

    if st.session_state.get("event_id"):
        st.success(f"Event created: {st.session_state.event_id}")
        if st.session_state.event_data and "critical_conditions" in st.session_state.event_data:
            with st.expander("📋 Critical Conditions Extracted"):
                st.json(st.session_state.event_data["critical_conditions"])


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

            # --- Создаем остальные компоненты ---
            aggregator = Aggregator()
            conflict_detector = ConflictDetector()
            decision_engine = DecisionEngine()
            authority_gate = AuthorityGate()
            state_machine = StateMachine()

            # --- Подготавливаем данные для департаментов ---
            event_data = st.session_state.event_data.copy()

            # Добавляем поля для департаментов
            event_data["situation"] = event_data.get("description", "Incident detected")
            event_data["time_to_event"] = 5
            event_data["action"] = "Analyze and respond"
            event_data["authorized"] = False
            event_data["decision_proposal"] = "Awaiting assessment"
            event_data["evidence"] = [
                f"Event type: {event_data.get('event_type', 'UNKNOWN')}",
                f"Severity: {event_data.get('severity', 'UNKNOWN')}",
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

            # --- ОЦЕНКА РИСКА (v0.2) ---
            risk_engine = RiskEngine()
            critical_conditions = event_data.get("critical_conditions", [])
            risk_assessment = risk_engine.evaluate_risk(critical_conditions)
            aggregated_state["risk_assessment"] = risk_assessment

            state_machine.detect_conflicts()
            conflict_result = conflict_detector.detect(aggregated_state)

            state_machine.formulate_decision()
            decision_proposal = decision_engine.formulate(aggregated_state, conflict_result)
            decision_proposal["risk_assessment"] = risk_assessment

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
    if st.session_state.get("department_results"):
        st.subheader("Department Assessments")
        for dept, result in st.session_state.department_results.items():
            with st.expander(f"📋 {dept}"):
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.json(result)

    if st.session_state.get("aggregated_state"):
        st.subheader("📊 Aggregated State")
        st.json(st.session_state.aggregated_state)

        # --- Отображение оценки риска (v0.2) ---
        if "risk_assessment" in st.session_state.aggregated_state:
            st.subheader("⚠️ Risk Assessment")
            risk_data = st.session_state.aggregated_state["risk_assessment"]
            if risk_data.get("overall_risk") == "CRITICAL":
                st.error(f"🚨 CRITICAL RISK: {risk_data.get('risk_count', 0)} risks identified")
            elif risk_data.get("overall_risk") == "HIGH":
                st.warning(f"⚠️ HIGH RISK: {risk_data.get('risk_count', 0)} risks identified")
            else:
                st.success(f"✅ LOW RISK: {risk_data.get('risk_count', 0)} risks identified")
            st.json(risk_data)

    if st.session_state.get("conflict_result"):
        st.subheader("⚠️ Conflict Detection")
        if st.session_state.conflict_result.get("has_conflicts"):
            st.warning("Conflicts detected!")
        else:
            st.success("No conflicts detected")
        st.json(st.session_state.conflict_result)


# --- TAB 3: DECISION ---
with tab3:
    st.header("Decision Authority")

    if st.session_state.get("decision_proposal"):
        st.subheader("Decision Proposal")
        st.json(st.session_state.decision_proposal)

    if st.session_state.get("authority_state"):
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

        if st.session_state.get("authorized") is True:
            st.success("✅ Decision Authorized")
            st.session_state.current_step = "completed"
        elif st.session_state.get("authorized") is False:
            st.error("❌ Decision Rejected")


# --- TAB 4: RECORD ---
with tab4:
    st.header("AVCS Decision Record")

    if st.session_state.current_step == "completed":
        if st.session_state.get("authorized"):
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
