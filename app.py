"""
Email Handler Multi-Agent System
Streamlit frontend voor email classificatie en response generatie
"""

import streamlit as st
from crew_setup import EmailHandlerCrew
from config import CATEGORIES, SENTIMENTS

# Page config
st.set_page_config(
    page_title="Email Handler AI",
    page_icon="📧",
    layout="wide"
)

# Title
st.title("📧 Email Handler Multi-Agent System")
st.markdown("Classificeer emails en genereer automatisch passende antwoorden met AI agents")

# Sidebar met info
with st.sidebar:
    st.header("ℹ️ Over dit systeem")
    st.markdown("""
    Dit systeem gebruikt 3 gespecialiseerde AI agents:
    
    **Agent 1: Classifier**
    - Classificeert email type
    - Detecteert spam
    
    **Agent 2: Sentiment Analyzer**
    - Analyseert sentiment
    - Bepaalt urgentie
    
    **Agent 3: Response Generator**
    - Genereert passend antwoord
    - Past tone aan op basis van classificatie
    """)
    
    st.divider()
    st.markdown("**Categorieën:**")
    for cat in CATEGORIES:
        st.markdown(f"• {cat}")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📨 Input Email")
    
    # Email input
    email_text = st.text_area(
        "Plak hier de email tekst:",
        height=300,
        placeholder="Beste ...,\n\nIk wil graag ...\n\nMet vriendelijke groet,\n..."
    )
    
    # Analyze button
    analyze_button = st.button("🔍 Analyseer Email", type="primary", use_container_width=True)

with col2:
    st.subheader("📊 Resultaten")
    
    if analyze_button:
        if not email_text.strip():
            st.warning("⚠️ Voer eerst een email in!")
        else:
            with st.spinner("🤖 Agents aan het werk..."):
                try:
                    # Initialize crew
                    crew = EmailHandlerCrew()
                    
                    # Process email
                    result = crew.process_email(email_text)
                    
                    # Display results
                    st.success("✅ Email succesvol geanalyseerd!")
                    
                    # Category
                    st.markdown("### 📋 Classificatie")
                    category = result.get('category', 'Onbekend')
                    
                    # Color code by category
                    if category == "Spam":
                        st.error(f"**Categorie:** {category}")
                    elif category == "Klacht":
                        st.warning(f"**Categorie:** {category}")
                    else:
                        st.info(f"**Categorie:** {category}")
                    
                    # Sentiment
                    st.markdown("### 😊 Sentiment")
                    sentiment = result.get('sentiment', 'Onbekend')
                    
                    if sentiment == "Positive":
                        st.success(f"**Sentiment:** {sentiment} 😊")
                    elif sentiment == "Negative":
                        st.error(f"**Sentiment:** {sentiment} 😠")
                    else:
                        st.info(f"**Sentiment:** {sentiment} 😐")
                    
                    # Response
                    st.markdown("### 💬 Gegenereerd Antwoord")
                    response = result.get('response', 'Geen antwoord gegenereerd')
                    
                    st.text_area(
                        "Concept antwoord:",
                        value=response,
                        height=200,
                        disabled=False,
                        help="Je kunt dit antwoord nog aanpassen voordat je het verstuurt"
                    )
                    
                    # Copy button
                    if st.button("📋 Kopieer Antwoord", use_container_width=True):
                        st.toast("Antwoord gekopieerd! ✅")
                    
                except Exception as e:
                    st.error(f"❌ Er ging iets mis: {str(e)}")
                    st.exception(e)
    else:
        st.info("👈 Voer een email in en klik op 'Analyseer Email'")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Gebouwd met CrewAI • Streamlit • OpenAI GPT-4</small>
</div>
""", unsafe_allow_html=True)
