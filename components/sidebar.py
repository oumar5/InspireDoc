import streamlit as st
from typing import Optional

def show_sidebar() -> str:
    """
    Affiche la sidebar avec navigation et statut système.
    
    Returns:
        str: La page sélectionnée par l'utilisateur
    """
    with st.sidebar:
        # Menu de navigation simplifié
        page = st.radio(
            "📍 Navigation",
            ["🏠 Accueil", "⚡ Génération", "⚙️ Paramètres", "ℹ️ À propos"],
            index=0,
            label_visibility="visible"
        )
        
        # Affichage du statut système
        st.markdown("---")
        st.markdown("**🔧 Statut Système**")
        
        _show_system_status()
        
        return page

def _show_system_status() -> None:
    """
    Affiche le statut du système dans la sidebar.
    """
    try:
        from core.services.document_service import DocumentService
        service = DocumentService()
        status = service.get_service_status()
        
        if status.get('service_initialized', False):
            st.success("✅ Service OK")
        else:
            st.error("❌ Service KO")
            
        if status.get('llm_connection', False):
            st.success("✅ LLM OK")
        else:
            st.warning("⚠️ LLM Config")
    except Exception:
        st.error("❌ Erreur init")