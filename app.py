"""
Email Handler Multi-Agent System
Streamlit frontend met 5-agent workflow visualization
"""

import streamlit as st
from crew_setup import EmailHandlerCrew
from config import CATEGORIES, URGENCY_LEVELS, SENTIMENTS, ROUTING_TEAMS
import json

# Page config
st.set_page_config(
    page_title="Email Handler AI",
    page_icon="📧",
    layout="wide"
)

# Title
st.title("📧 Email Handler Multi-Agent System")
st.markdown("**5 gespecialiseerde AI agents** werken samen om emails te analyseren en beantwoorden")

# Sidebar met info
with st.sidebar:
    st.header("ℹ️ Multi-Agent Workflow")
    
    st.markdown("### 🔄 Fase 1: Parallel Analysis")
    st.markdown("""
    **Agent 1: Categorizer** 📋
    - Classificeert email type
    
    **Agent 2: Urgency Analyzer** ⏰
    - Bepaalt urgentie & deadlines
    
    **Agent 3: Sentiment Analyzer** 😊
    - Analyseert emotie & risico's
    
    *Deze 3 draaien parallel!*
    """)
    
    st.markdown("### 🎯 Fase 2: Routing Decision")
    st.markdown("""
    **Agent 4: Router (Orchestrator)** 🎯
    - Gebruikt output van Agent 1, 2, 3
    - Bepaalt team & prioriteit
    - Detecteert risico's
    """)
    
    st.markdown("### 💬 Fase 3: Response")
    st.markdown("""
    **Agent 5: Response Generator** ✉️
    - Gebruikt routing beslissing
    - Genereert passend antwoord
    """)
    
    st.divider()
    
    with st.expander("📋 Categorieën"):
        for cat in CATEGORIES:
            st.markdown(f"• {cat}")
    
    with st.expander("⏰ Urgency Levels"):
        for urg in URGENCY_LEVELS:
            st.markdown(f"• {urg}")
    
    with st.expander("🎯 Routing Teams"):
        for team in ROUTING_TEAMS:
            st.markdown(f"• {team}")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📨 Input Email")
    
    # Email input
    email_text = st.text_area(
        "Plak hier de email tekst:",
        height=400,
        placeholder="""Beste klantenservice,

Ik ben zeer ontevreden over jullie product...

Met vriendelijke groet,
Jan Jansen""",
        help="Plak een complete email inclusief aanhef en afsluiting"
    )
    
    # Analyze button
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        analyze_button = st.button("🔍 Analyseer Email", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🧪 Load Test Email", use_container_width=True):
            email_text = """Geachte heer/mevrouw,

Dit is nu de DERDE keer dat ik contact opneem en NIEMAND reageert!
Mijn laptop is kapot en jullie doen er NIETS aan. Dit is ONACCEPTABEL.

Als ik morgen om 12:00 geen reactie heb, schakel ik een advocaat in.
Ik wil mijn geld terug OF een werkend product. Nu meteen!

Jan Jansen"""
            st.rerun()

with col2:
    st.subheader("📊 Multi-Agent Analysis")
    
    if analyze_button:
        if not email_text.strip():
            st.warning("⚠️ Voer eerst een email in!")
        else:
            with st.spinner("🤖 Multi-agent system processing..."):
                try:
                    # Initialize crew
                    crew = EmailHandlerCrew()
                    
                    # Process email
                    result = crew.process_email(email_text)
                    
                    # Check for errors
                    if 'error' in result:
                        st.error(f"❌ Error: {result['error']}")
                        st.stop()
                    
                    # Display results
                    st.success("✅ Email succesvol verwerkt door 5 agents!")
                    
                    # ================================================
                    # FASE 1 RESULTS: Parallel Analysis
                    # ================================================
                    st.markdown("### 🔄 Fase 1: Parallel Analysis")
                    
                    col_cat, col_urg, col_sent = st.columns(3)
                    
                    # Category
                    with col_cat:
                        st.markdown("#### 📋 Category")
                        category_data = result.get('category', {})
                        category = category_data.get('category', 'Unknown')
                        confidence = category_data.get('confidence', 0)
                        
                        if category == "Spam":
                            st.error(f"**{category}**")
                        elif category == "Klacht":
                            st.warning(f"**{category}**")
                        else:
                            st.info(f"**{category}**")
                        
                        st.metric("Confidence", f"{confidence:.0%}")
                        
                        with st.expander("Details"):
                            st.json(category_data)
                    
                    # Urgency
                    with col_urg:
                        st.markdown("#### ⏰ Urgency")
                        urgency_data = result.get('urgency', {})
                        urgency = urgency_data.get('urgency_level', 'Unknown')
                        response_time = urgency_data.get('recommended_response_time', 0)
                        
                        if urgency == "Critical":
                            st.error(f"**{urgency}**")
                        elif urgency == "High":
                            st.warning(f"**{urgency}**")
                        elif urgency == "Medium":
                            st.info(f"**{urgency}**")
                        else:
                            st.success(f"**{urgency}**")
                        
                        st.metric("Response Time", f"{response_time}h")
                        
                        if urgency_data.get('has_deadline'):
                            st.caption(f"⏰ Deadline: {urgency_data.get('deadline_date')}")
                        
                        with st.expander("Details"):
                            st.json(urgency_data)
                    
                    # Sentiment
                    with col_sent:
                        st.markdown("#### 😊 Sentiment")
                        sentiment_data = result.get('sentiment', {})
                        sentiment = sentiment_data.get('sentiment', 'Unknown')
                        escalation = sentiment_data.get('escalation_risk', False)
                        
                        sentiment_emoji = {
                            'Positive': '😊',
                            'Neutral': '😐',
                            'Negative': '😠',
                            'Very_Negative': '😡'
                        }
                        
                        emoji = sentiment_emoji.get(sentiment, '❓')
                        
                        if sentiment == "Very_Negative":
                            st.error(f"**{sentiment}** {emoji}")
                        elif sentiment == "Negative":
                            st.warning(f"**{sentiment}** {emoji}")
                        elif sentiment == "Positive":
                            st.success(f"**{sentiment}** {emoji}")
                        else:
                            st.info(f"**{sentiment}** {emoji}")
                        
                        if escalation:
                            st.error("⚠️ Escalation Risk!")
                        
                        with st.expander("Details"):
                            st.json(sentiment_data)
                    
                    st.divider()
                    
                    # ================================================
                    # FASE 2 RESULTS: Routing Decision
                    # ================================================
                    st.markdown("### 🎯 Fase 2: Routing Decision")
                    
                    routing_data = result.get('routing', {})
                    
                    col_route1, col_route2 = st.columns([1, 1])
                    
                    with col_route1:
                        st.markdown("#### 📍 Routing")
                        team = routing_data.get('route_to_team', 'Unknown')
                        priority = routing_data.get('priority', 0)
                        sla = routing_data.get('sla_hours', 0)
                        
                        st.info(f"**Team:** {team}")
                        
                        priority_color = {
                            1: "🔴",
                            2: "🟠", 
                            3: "🟡",
                            4: "🟢",
                            5: "🔵"
                        }
                        st.metric(
                            "Priority", 
                            f"{priority_color.get(priority, '⚪')} {priority}",
                            help="1 = Hoogste, 5 = Laagste"
                        )
                        st.metric("SLA", f"{sla} hours")
                    
                    with col_route2:
                        st.markdown("#### ⚠️ Flags")
                        
                        if routing_data.get('requires_escalation'):
                            st.error("🚨 **Escalation Required**")
                        
                        if routing_data.get('requires_manager_approval'):
                            st.warning("👔 **Manager Approval Needed**")
                        
                        risk_flags = routing_data.get('risk_flags', [])
                        if risk_flags:
                            st.warning(f"⚠️ **Risk Flags:** {', '.join(risk_flags)}")
                        
                        if not routing_data.get('requires_escalation') and not risk_flags:
                            st.success("✅ Standard processing")
                    
                    with st.expander("📋 Routing Reasoning"):
                        st.write(routing_data.get('reasoning', 'No reasoning provided'))
                    
                    st.divider()
                    
                    # ================================================
                    # FASE 3 RESULTS: Response
                    # ================================================
                    st.markdown("### 💬 Fase 3: Generated Response")
                    
                    response_data = result.get('response', {})
                    response_text = response_data.get('response_text', 'No response generated')
                    tone = response_data.get('tone', 'Unknown')
                    response_type = response_data.get('response_type', 'Unknown')
                    
                    col_resp1, col_resp2 = st.columns([2, 1])
                    
                    with col_resp1:
                        st.text_area(
                            "Draft Email Response:",
                            value=response_text,
                            height=300,
                            help="Je kunt dit antwoord nog aanpassen voordat je het verstuurt"
                        )
                    
                    with col_resp2:
                        st.markdown("#### 📝 Response Info")
                        st.info(f"**Tone:** {tone}")
                        st.info(f"**Type:** {response_type}")
                        
                        if response_data.get('includes_apology'):
                            st.caption("✅ Includes apology")
                        if response_data.get('includes_solution'):
                            st.caption("✅ Includes solution")
                        if response_data.get('follow_up_required'):
                            st.caption(f"📅 Follow-up: {response_data.get('follow_up_date')}")
                        if response_data.get('cc_manager'):
                            st.caption("👔 CC Manager")
                    
                    # Action buttons
                    col_action1, col_action2, col_action3 = st.columns(3)
                    with col_action1:
                        if st.button("📋 Copy Response", use_container_width=True):
                            st.toast("Response copied! ✅")
                    with col_action2:
                        if st.button("✏️ Edit Response", use_container_width=True):
                            st.info("Edit mode activated")
                    with col_action3:
                        if st.button("📤 Send Email", use_container_width=True):
                            st.success("Email sent! ✅")
                    
                except Exception as e:
                    st.error(f"❌ Er ging iets mis: {str(e)}")
                    with st.expander("🐛 Debug Info"):
                        st.exception(e)
    else:
        st.info("👈 Voer een email in en klik op 'Analyseer Email'")
        
        # Show example
        with st.expander("📧 Voorbeeld Email"):
            st.code("""Geachte heer/mevrouw,

Dit is nu de DERDE keer dat ik contact opneem!
Mijn product is kapot en niemand reageert.

Als ik morgen geen reactie heb, schakel ik een advocaat in.

Met vriendelijke groet,
Jan Jansen""")

# Footer
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**🤖 5 Agents**")
    st.caption("Categorizer • Urgency • Sentiment • Router • Responder")

with col_footer2:
    st.markdown("**⚡ Hybrid Workflow**")
    st.caption("Parallel Analysis → Sequential Decision")

with col_footer3:
    st.markdown("**🔧 Tech Stack**")
    st.caption("CrewAI • Streamlit • GPT-4o-mini")
