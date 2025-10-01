"""
Insurance Claims Multi-Agent System - Streamlit UI

Professional interface for insurance claim processing with 5-agent workflow visualization.
"""

import streamlit as st
from crew_setup_new import InsuranceClaimsCrew
import json

# Page config
st.set_page_config(
    page_title="Insurance Claims AI",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🏥 Insurance Claims Multi-Agent System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated claim triage & customer communication powered by 5 specialized AI agents</div>', unsafe_allow_html=True)

# Sidebar with workflow info
with st.sidebar:
    st.header("🔄 Multi-Agent Workflow")
    
    st.markdown("### 📊 Phase 1: Parallel Analysis")
    st.markdown("""
    **Agent 1: Type Classifier** 📋
    - Identifies claim type
    - Extracts policy & date
    
    **Agent 2: Urgency & Amount** ⏰💰
    - Assesses urgency level
    - Extracts damage amount
    
    **Agent 3: Fraud Detector** 🚨
    - Analyzes fraud risk
    - Detects red flags
    
    *These 3 agents run independently!*
    """)
    
    st.markdown("### 🎯 Phase 2: Smart Routing")
    st.markdown("""
    **Agent 4: Router (Orchestrator)** 🎯
    - Combines all analyses
    - Makes routing decision
    - Sets priority & SLA
    """)
    
    st.markdown("### 💬 Phase 3: Response")
    st.markdown("""
    **Agent 5: Response Generator** ✉️
    - Selects template (A/B/C/D)
    - Generates customer email
    - Professional tone
    """)
    
    st.divider()
    
    with st.expander("📋 Claim Types"):
        st.markdown("• Auto\n• Woning\n• Inboedel\n• Aansprakelijkheid")
    
    with st.expander("⚡ Routing Paths"):
        st.markdown("• Auto-Approve (<€750, low risk)\n• Junior Adjuster\n• Standard Adjuster\n• Senior Adjuster\n• SIU Investigation")
    
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Version:** 1.0  
        **Model:** GPT-4o-mini  
        **Framework:** CrewAI  
        **Target:** 60-70% auto-approval rate
        """)

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📨 Submit Insurance Claim")
    
    # Claim input
    claim_text = st.text_area(
        "Enter claim details:",
        height=350,
        placeholder="""Beste verzekering,

Gisteren ben ik aangereden op de parkeerplaats. 
De andere auto heeft mijn bumper geraakt.

Geschatte schade: €600
Polisnummer: AUTO-2024-12345
Datum: 30 september 2025

Met vriendelijke groet,
Jan Janssen""",
        help="Include: incident description, amount, policy number, date"
    )
    
    # Action buttons
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        process_button = st.button("🔍 Process Claim", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🧪 Load Test Claim", use_container_width=True):
            claim_text = """Beste verzekering,

Gisteren heb ik een kleine kras op mijn bumper gekregen door een winkelwagentje 
op de parkeerplaats van de Albert Heijn. De schade is minimaal, alleen lakschade.

Geschatte schade: ongeveer €400
Polisnummer: AUTO-2024-12345
Datum incident: 30 september 2025
Kenteken: AA-123-BB

Met vriendelijke groet,
Jan Janssen
jan.janssen@email.nl"""
            st.rerun()

with col2:
    st.subheader("📊 Multi-Agent Analysis Results")
    
    if process_button:
        if not claim_text.strip():
            st.warning("⚠️ Please enter a claim first!")
        else:
            with st.spinner("🤖 Multi-agent system processing claim..."):
                try:
                    # Initialize crew
                    crew = InsuranceClaimsCrew()
                    
                    # Process claim
                    result = crew.process_claim(claim_text)
                    
                    # Check for errors
                    if 'error' in result:
                        st.error(f"❌ Error: {result['error']}")
                        st.stop()
                    
                    # Display success
                    st.success("✅ Claim successfully processed by 5 agents!")
                    
                    # ================================================
                    # PHASE 1 RESULTS: Parallel Analysis
                    # ================================================
                    st.markdown("### 🔄 Phase 1: Parallel Analysis")
                    
                    col_type, col_urg, col_fraud = st.columns(3)
                    
                    # Claim Type
                    with col_type:
                        st.markdown("#### 📋 Claim Type")
                        type_data = result.get('claim_type', {})
                        claim_type = type_data.get('type', 'Unknown')
                        confidence = type_data.get('confidence', 0)
                        
                        # Color coding
                        if confidence > 0.8:
                            st.success(f"**{claim_type}**")
                        elif confidence > 0.5:
                            st.info(f"**{claim_type}**")
                        else:
                            st.warning(f"**{claim_type}**")
                        
                        st.metric("Confidence", f"{confidence:.0%}")
                        
                        policy = type_data.get('policy_number')
                        if policy:
                            st.caption(f"📄 Policy: {policy}")
                        
                        with st.expander("Details"):
                            st.json(type_data)
                    
                    # Urgency & Amount
                    with col_urg:
                        st.markdown("#### ⏰💰 Urgency & Amount")
                        urg_data = result.get('urgency_amount', {})
                        urgency = urg_data.get('urgency_level', 'Unknown')
                        amount = urg_data.get('amount_euros', 0)
                        
                        # Urgency color coding
                        if urgency == "Critical":
                            st.error(f"**{urgency}**")
                        elif urgency == "High":
                            st.warning(f"**{urgency}**")
                        elif urgency == "Medium":
                            st.info(f"**{urgency}**")
                        else:
                            st.success(f"**{urgency}**")
                        
                        st.metric("Amount", f"€{amount:,.2f}" if amount else "Unknown")
                        
                        if urg_data.get('is_total_loss'):
                            st.error("⚠️ Total Loss Detected")
                        
                        with st.expander("Details"):
                            st.json(urg_data)
                    
                    # Fraud Risk
                    with col_fraud:
                        st.markdown("#### 🚨 Fraud Risk")
                        fraud_data = result.get('fraud_risk', {})
                        risk_level = fraud_data.get('risk_level', 'Unknown')
                        risk_score = fraud_data.get('risk_score', 0)
                        
                        # Risk level color coding
                        if risk_level == "High":
                            st.error(f"**{risk_level}**")
                        elif risk_level == "Medium":
                            st.warning(f"**{risk_level}**")
                        else:
                            st.success(f"**{risk_level}**")
                        
                        st.metric("Risk Score", f"{risk_score:.2f}")
                        
                        red_flags = fraud_data.get('red_flags', [])
                        if red_flags:
                            st.error(f"🚩 {len(red_flags)} Red Flag(s)")
                        
                        with st.expander("Details"):
                            st.json(fraud_data)
                    
                    st.divider()
                    
                    # ================================================
                    # PHASE 2 RESULTS: Routing Decision
                    # ================================================
                    st.markdown("### 🎯 Phase 2: Routing Decision")
                    
                    routing_data = result.get('routing', {})
                    
                    col_route1, col_route2 = st.columns([1, 1])
                    
                    with col_route1:
                        st.markdown("#### 📍 Routing Details")
                        route_path = routing_data.get('route_path', 'Unknown')
                        team = routing_data.get('route_to_team', 'Unknown')
                        priority = routing_data.get('priority', 0)
                        sla = routing_data.get('sla_hours', 0)
                        
                        # Route path color coding
                        if route_path == "Auto-Approve":
                            st.success(f"**Path:** {route_path}")
                        elif "SIU" in route_path:
                            st.error(f"**Path:** {route_path}")
                        elif "Senior" in route_path:
                            st.warning(f"**Path:** {route_path}")
                        else:
                            st.info(f"**Path:** {route_path}")
                        
                        st.info(f"**Team:** {team}")
                        
                        # Priority indicator
                        priority_colors = {
                            1: "🔴",
                            2: "🟠",
                            3: "🟡",
                            4: "🟢",
                            5: "🔵"
                        }
                        st.metric(
                            "Priority",
                            f"{priority_colors.get(priority, '⚪')} P{priority}",
                            help="1 = Highest, 5 = Lowest"
                        )
                        st.metric("SLA", f"{sla} hours")
                    
                    with col_route2:
                        st.markdown("#### ⚠️ Flags & Requirements")
                        
                        if routing_data.get('requires_manager_approval'):
                            st.warning("👔 **Manager Approval Required**")
                        
                        if routing_data.get('requires_inspection'):
                            st.info("🔍 **Inspection Needed**")
                        
                        escalation_flags = routing_data.get('escalation_flags', [])
                        if escalation_flags:
                            st.error(f"🚩 **Escalation Flags:**")
                            for flag in escalation_flags:
                                st.caption(f"• {flag}")
                        
                        if not escalation_flags and not routing_data.get('requires_manager_approval'):
                            st.success("✅ Standard processing")
                    
                    with st.expander("📋 Routing Reasoning"):
                        st.write(routing_data.get('reasoning', 'No reasoning provided'))
                    
                    st.divider()
                    
                    # ================================================
                    # PHASE 3 RESULTS: Customer Response
                    # ================================================
                    st.markdown("### 💬 Phase 3: Customer Response")
                    
                    response_data = result.get('response', {})
                    response_text = response_data.get('response_text', 'No response generated')
                    template = response_data.get('template_used', 'Unknown')
                    tone = response_data.get('tone', 'Unknown')
                    claim_ref = response_data.get('claim_reference_number', 'Unknown')
                    
                    col_resp1, col_resp2 = st.columns([2, 1])
                    
                    with col_resp1:
                        st.text_area(
                            "Generated Email Response:",
                            value=response_text,
                            height=350,
                            help="This email will be sent to the customer"
                        )
                    
                    with col_resp2:
                        st.markdown("#### 📝 Response Info")
                        
                        # Template badge
                        template_colors = {
                            "A": "🟢",
                            "B": "🔵",
                            "C": "🟡",
                            "D": "🔴"
                        }
                        st.info(f"**Template:** {template_colors.get(template, '⚪')} {template}")
                        st.info(f"**Tone:** {tone}")
                        st.info(f"**Reference:** {claim_ref}")
                        
                        if response_data.get('includes_approval'):
                            st.success("✅ Includes approval")
                        
                        processing_time = response_data.get('estimated_processing_time', 'Unknown')
                        st.caption(f"⏱️ Processing: {processing_time}")
                    
                    # Action buttons for response
                    st.markdown("#### 📤 Actions")
                    col_action1, col_action2, col_action3 = st.columns(3)
                    
                    with col_action1:
                        if st.button("📋 Copy Response", use_container_width=True):
                            st.toast("Response copied to clipboard! ✅", icon="📋")
                    
                    with col_action2:
                        if st.button("✏️ Edit Response", use_container_width=True):
                            st.info("Edit mode would open here")
                    
                    with col_action3:
                        if st.button("📤 Send Email", use_container_width=True):
                            st.success("Email would be sent! ✅")
                    
                    # Download JSON
                    st.divider()
                    st.download_button(
                        label="📥 Download Complete Analysis (JSON)",
                        data=json.dumps(result, indent=2),
                        file_name=f"claim_analysis_{claim_ref}.json",
                        mime="application/json"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error processing claim: {str(e)}")
                    with st.expander("🐛 Debug Info"):
                        st.exception(e)
    else:
        st.info("👈 Enter a claim and click 'Process Claim' to start analysis")
        
        # Show example claims
        with st.expander("📧 Example Claims"):
            st.markdown("**Auto Claim (Should Auto-Approve):**")
            st.code("""Beste verzekering,

Kleine kras op bumper door winkelwagentje.
Schade: €400
Polisnummer: AUTO-2024-12345""")
            
            st.markdown("**High Value Claim (Senior Review):**")
            st.code("""Ernstige aanrijding, auto total loss.
Cataloguswaarde: €28.000
Polisnummer: AUTO-2024-67890""")
            
            st.markdown("**Suspicious Claim (SIU Investigation):**")
            st.code("""Laptop gestolen uit auto.
Schatting: €2.200
Polis vorige week afgesloten.
Weet niet meer waar geparkeerd.""")

# Footer
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**🤖 5 Specialized Agents**")
    st.caption("Type • Urgency/Amount • Fraud • Router • Response")

with col_footer2:
    st.markdown("**⚡ Hybrid Workflow**")
    st.caption("Parallel Analysis → Sequential Decision → Response")

with col_footer3:
    st.markdown("**🎯 Target Metrics**")
    st.caption("60-70% Auto-Approval • <30s Processing • >95% Accuracy")
