"""
Insurance Claims Multi-Agent System - Streamlit UI (Clean White)

Simple white theme with clear layout - FIXED: Response updates properly + black text
"""

import streamlit as st
from crew_setup_openai import InsuranceClaimsPipeline
import json

# Page config
st.set_page_config(
    page_title="Schadeclaim Systeem",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS - Clean white theme + black text in response
st.markdown("""
<style>
    /* Agent boxes with colored borders */
    .agent-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 5px;
        border: 3px solid #dee2e6;
        min-height: 180px;
    }
    .agent-parallel {
        border-color: #2196F3;
        background-color: #e3f2fd;
    }
    .agent-router {
        border-color: #FF9800;
        background-color: #fff3e0;
    }
    .agent-response {
        border-color: #4CAF50;
        background-color: #e8f5e9;
    }
    
    /* Big arrows */
    .big-arrow {
        font-size: 3rem;
        text-align: center;
        color: #666;
        margin: 20px 0;
        font-weight: bold;
    }
    
    /* Make disabled textarea text black instead of gray */
    textarea:disabled {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏥 Schadeclaim Verwerkingssysteem")
st.caption("Geautomatiseerde claimverwerking met multi-agent AI")

st.divider()

# ============================================================================
# TOP SECTION: INPUT (LEFT) + RESPONSE (RIGHT)
# ============================================================================

col_input, col_response = st.columns([1, 1])

with col_input:
    st.subheader("📧 Schadeclaim E-mail")
    
    claim_text = st.text_area(
        "Voer claim e-mail in:",
        height=400,
        placeholder="""Beste verzekering,

Gisteren heb ik een kleine kras op mijn bumper gekregen door een winkelwagentje 
op de parkeerplaats. De schade is minimaal.

Geschatte schade: €400
Polisnummer: AUTO-2024-12345
Datum incident: 30 september 2025

Met vriendelijke groet,
Jan Janssen""",
        key="claim_input"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        process_btn = st.button("🔍 Verwerk Claim", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🧪 Test Laden", use_container_width=True):
            st.session_state.test_claim = """Beste verzekering,

Gisteren heb ik een kleine kras op mijn bumper gekregen door een winkelwagentje 
op de parkeerplaats. De schade is minimaal.

Geschatte schade: €400
Polisnummer: AUTO-2024-12345
Datum incident: 30 september 2025

Met vriendelijke groet,
Jan Janssen"""
            st.rerun()
    
    # Load test claim if button was clicked
    if 'test_claim' in st.session_state:
        claim_text = st.session_state.test_claim
        del st.session_state.test_claim

with col_response:
    st.subheader("📨 Respons van Verzekeraar")
    
    if 'result' in st.session_state:
        response_data = st.session_state.result.get('response', {})
        response_text = response_data.get('response_text', '')
        claim_ref = response_data.get('claim_reference_number', 'N/A')
        
        # FIXED: Use unique key per claim to force update
        st.text_area(
            "Gegenereerde e-mail aan klant:",
            value=response_text,
            height=400,
            key=f"response_{claim_ref}",  # Unique key per claim!
            disabled=True
        )
        
        # Response metadata
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            template = response_data.get('template_used', 'Unknown')
            template_labels = {
                "A": "🟢 Auto-Goedkeurd",
                "B": "🔵 Standaard",
                "C": "🟡 Extra Check",
                "D": "🔴 Hoogste Prioriteit"
            }
            st.caption(f"**Template:** {template_labels.get(template, template)}")
        with col_meta2:
            st.caption(f"**Ref:** {claim_ref}")
    else:
        st.info("👈 Voer een claim in en klik 'Verwerk Claim'")
        st.caption("De respons van de verzekeraar verschijnt hier...")

# Process claim
if process_btn:
    if not claim_text.strip():
        st.warning("⚠️ Voer eerst een claim in!")
    else:
        with st.spinner("🤖 Multi-agent systeem aan het werk..."):
            try:
                pipeline = InsuranceClaimsPipeline()
                result = pipeline.process_claim(claim_text)
                
                if 'error' in result:
                    st.error(f"❌ Fout: {result['error']}")
                else:
                    # Store result and immediately rerun
                    st.session_state.result = result
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.divider()

# ============================================================================
# BOTTOM SECTION: AGENT WORKFLOW VISUALIZATION
# ============================================================================

if 'result' in st.session_state:
    result = st.session_state.result
    meta = result.get('meta', {})
    
    st.subheader("🔄 Multi-Agent Workflow Visualisatie")
    
    # Performance metrics
    col_perf1, col_perf2, col_perf3 = st.columns(3)
    with col_perf1:
        st.metric("⚡ Verwerkingstijd", f"{meta.get('processing_time_seconds', 0):.1f}s")
    with col_perf2:
        st.metric("🤖 LLM Calls", meta.get('llm_calls_used', 0))
    with col_perf3:
        st.metric("✅ Status", "Succesvol")
    
    st.markdown("---")
    
    # ================================================
    # FASE 1: PARALLELLE AGENTS
    # ================================================
    st.markdown("### 📊 Fase 1: Parallelle Analyse")
    st.caption("Deze 3 agents werken tegelijk")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="agent-box agent-parallel"><strong>Agent 1: Type & Bedrag</strong><br>📋💰</div>', unsafe_allow_html=True)
        type_data = result.get('claim_type', {})
        st.markdown(f"**Type:** {type_data.get('type', 'Unknown')}")
        amount = type_data.get('amount_euros', 0)
        st.markdown(f"**Bedrag:** €{amount:,.2f}" if amount else "**Bedrag:** Onbekend")
        st.markdown(f"**Confidence:** {type_data.get('confidence', 0):.0%}")
        
        with st.expander("Details"):
            st.json(type_data)
    
    with col2:
        st.markdown('<div class="agent-box agent-parallel"><strong>Agent 2: Urgentie</strong><br>⏰</div>', unsafe_allow_html=True)
        urg_data = result.get('urgency', {})
        urgency = urg_data.get('urgency_level', 'Unknown')
        
        if urgency == "Critical":
            st.error(f"**Urgentie:** {urgency}")
        elif urgency == "High":
            st.warning(f"**Urgentie:** {urgency}")
        else:
            st.success(f"**Urgentie:** {urgency}")
        
        st.markdown(f"**SLA:** {urg_data.get('sla_hours', 0)}h")
        
        with st.expander("Details"):
            st.json(urg_data)
    
    with col3:
        st.markdown('<div class="agent-box agent-parallel"><strong>Agent 3: Fraude</strong><br>🚨</div>', unsafe_allow_html=True)
        fraud_data = result.get('fraud_risk', {})
        risk_level = fraud_data.get('risk_level', 'Unknown')
        
        if risk_level == "High":
            st.error(f"**Risico:** {risk_level}")
        elif risk_level == "Medium":
            st.warning(f"**Risico:** {risk_level}")
        else:
            st.success(f"**Risico:** {risk_level}")
        
        st.markdown(f"**Score:** {fraud_data.get('risk_score', 0):.2f}")
        
        red_flags = fraud_data.get('red_flags', [])
        if red_flags:
            st.error(f"🚩 {len(red_flags)} rode vlag(gen)")
        
        with st.expander("Details"):
            st.json(fraud_data)
    
    # BIG ARROW
    st.markdown('<div class="big-arrow">⬇️</div>', unsafe_allow_html=True)
    
    # ================================================
    # FASE 2: ROUTER
    # ================================================
    st.markdown("### 🎯 Fase 2: Router (Pure Python)")
    st.caption("Combineert alle analyses en maakt routeringsbeslissing")
    
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        st.markdown('<div class="agent-box agent-router"><strong>Agent 4: Router</strong><br>🎯</div>', unsafe_allow_html=True)
        
        routing_data = result.get('routing', {})
        route_path = routing_data.get('route_path', 'Unknown')
        team = routing_data.get('route_to_team', 'Unknown')
        priority = routing_data.get('priority', 0)
        
        if route_path == "Auto-Goedkeuring":
            st.success(f"**Route:** {route_path}")
        elif "Fraude" in route_path:
            st.error(f"**Route:** {route_path}")
        else:
            st.info(f"**Route:** {route_path}")
        
        st.markdown(f"**Team:** {team}")
        priority_colors = {1: "🔴", 2: "🟠", 3: "🟡"}
        st.markdown(f"**Prioriteit:** {priority_colors.get(priority, '⚪')} P{priority}")
        
        with st.expander("Routing Redenering"):
            st.write(routing_data.get('reasoning', 'Geen redenering'))
        
        with st.expander("Details"):
            st.json(routing_data)
    
    # BIG ARROW
    st.markdown('<div class="big-arrow">⬇️</div>', unsafe_allow_html=True)
    
    # ================================================
    # FASE 3: RESPONSE GENERATOR
    # ================================================
    st.markdown("### 💬 Fase 3: Respons Generatie")
    st.caption("Genereert empathische respons naar klant")
    
    col_center2 = st.columns([1, 2, 1])
    with col_center2[1]:
        st.markdown('<div class="agent-box agent-response"><strong>Agent 5: Response Generator</strong><br>✉️</div>', unsafe_allow_html=True)
        
        response_data = result.get('response', {})
        template = response_data.get('template_used', 'Unknown')
        tone = response_data.get('tone', 'Unknown')
        
        st.markdown(f"**Template:** {template}")
        st.markdown(f"**Toon:** {tone}")
        
        if response_data.get('llm_enhanced'):
            st.success("✨ Empathisch versterkt (LLM)")
        
        if response_data.get('includes_approval'):
            st.success("✅ Bevat goedkeuring")
        
        with st.expander("Details"):
            st.json(response_data)
    
    st.markdown("---")
    
    # Download JSON
    col_download = st.columns([2, 1, 2])
    with col_download[1]:
        st.download_button(
            label="📥 Download Analyse (JSON)",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name=f"claim_{response_data.get('claim_reference_number', 'unknown')}.json",
            mime="application/json",
            use_container_width=True
        )

else:
    st.info("👆 Verwerk een claim om de workflow te zien")

# Footer
st.divider()
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption("🤖 Multi-Agent AI | 3 Parallel + Router + Response")
with col_f2:
    st.caption("⚡ Performance | ~30-50s | 4 LLM calls")
with col_f3:
    st.caption("🎯 Production Ready | Pydantic validated")
