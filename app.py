import streamlit as st
import threading
import time
from vata_sdk.wrappers import VATAGovernedAgentWrapper

st.set_page_config(page_title="VATA Command Center", page_icon="🛡️", layout="wide")

SECRET_KEY = b"VATA_DASHBOARD_SUPER_SECRET_KEY_2026"
WORKSPACE = "./vata_safe_zone"
gateway = VATAGovernedAgentWrapper(WORKSPACE, SECRET_KEY)

st.title("🛡️ VATA Core Kernel Engine")
st.subheader("Autonomous Agent Zero-Trust Execution Command Center")
st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Configure Agent Boundary")
    session_id = st.text_input("Session Identifier", value="enterprise_session_101")
    max_calls = st.slider("Max Permitted Tool Calls", min_value=1, max_value=20, value=5)
    
    st.markdown("### Resource Execution Profile")
    run_mode = st.radio(
        "Select Execution Scenario Simulation:",
        ("Standard Secure Session", "Exploit Vector A (Nested Bracket Template Injection)", "Exploit Vector B (Permissive Deserialization All-Access)")
    )
    
    execute_trigger = st.button("Deploy Governed Agent Loop", type="primary")

with col2:
    st.header("2. Live Kernel Interception Stream")
    status_box = st.empty()
    
    if execute_trigger:
        status_box.info("Initializing isolated VATA process thread context...")
        
        def simulated_agent(session):
            time.sleep(0.5)
            if run_mode == "Standard Secure Session":
                session.intercept_module_invocation("math.sqrt")
                session.verify_and_log_call()
                time.sleep(0.5)
                session.intercept_module_invocation("math.ceil")
                session.verify_and_log_call()
                return "Operation completed without configuration drift."
                
            elif run_mode == "Exploit Vector A (Nested Bracket Template Injection)":
                session.intercept_module_invocation("math.sqrt")
                session.verify_and_log_call()
                malicious_prompt = "{user_input:{malicious_attribute_lookup}}"
                gateway.sanitize_input_template(malicious_prompt)
                return "Unreachable code due to perimeter block."
                
            elif run_mode == "Exploit Vector B (Permissive Deserialization All-Access)":
                attack_config = {"allowed_objects": "all"}
                gateway.enforce_serialization_boundary(attack_config)
                return "Unreachable code due to serialization fence block."

        result = gateway.execute_governed_task(
            session_id=session_id,
            allowed_modules=["math"],
            max_calls=max_calls,
            agent_run_callable=simulated_agent
        )
        
        if result["status"] == "SUCCESS":
            status_box.success("Execution Safe: Thread Boundary Closed Safely.")
            st.metric(label="Runtime Status", value="CLEAN / VERIFIED")
            st.json(result)
        else:
            status_box.error("Security Breach Neutralized: Hard Boundary Imposed.")
            st.metric(label="Runtime Status", value="BREACH DETECTED & TERMINATED", delta="- CRITICAL")
            st.warning(f"Intercepted Payload Exception: {result['error']}")
            st.json(result)
