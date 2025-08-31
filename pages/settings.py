import streamlit as st
import os
from typing import Dict, Any

def show_settings_interface():
    """
    Interface des paramètres de l'application.
    """
    st.header("⚙️ Paramètres")
    
    # Configuration LLM
    show_llm_settings()
    
    # Configuration des fichiers
    show_file_settings()
    
    # Configuration de l'interface
    show_ui_settings()
    
    # Informations système
    show_system_info()

def show_llm_settings():
    """
    Paramètres du modèle de langage.
    """
    st.subheader("🤖 Configuration LLM")
    
    with st.expander("Configuration GPT-4o", expanded=True):
        # Variables d'environnement actuelles
        current_api_key = os.getenv("GPT4O_API_KEY", "")
        current_endpoint = os.getenv("GPT4O_ENDPOINT", "")
        
        # Affichage sécurisé de la clé API
        if current_api_key:
            masked_key = current_api_key[:8] + "*" * (len(current_api_key) - 12) + current_api_key[-4:] if len(current_api_key) > 12 else "*" * len(current_api_key)
            st.success(f"✅ Clé API configurée: {masked_key}")
        else:
            st.error("❌ Clé API non configurée")
        
        if current_endpoint:
            st.success(f"✅ Endpoint configuré: {current_endpoint}")
        else:
            st.error("❌ Endpoint non configuré")
        
        st.info("""
        **Configuration requise:**
        
        Pour utiliser InspireDoc, vous devez définir les variables d'environnement suivantes:
        
        ```bash
        export GPT4O_API_KEY="votre_cle_api"
        export GPT4O_ENDPOINT="https://votre-endpoint.openai.azure.com"
        ```
        
        Ou les ajouter à un fichier `.env` dans le répertoire racine.
        """)
    
    # Paramètres par défaut du modèle
    with st.expander("Paramètres par défaut du modèle"):
        col1, col2 = st.columns(2)
        
        with col1:
            default_temperature = st.slider(
                "Température par défaut",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="Contrôle la créativité du modèle"
            )
            
            default_max_tokens = st.number_input(
                "Tokens maximum par défaut",
                min_value=500,
                max_value=4000,
                value=2000,
                step=100,
                help="Longueur maximale de la génération"
            )
        
        with col2:
            default_top_p = st.slider(
                "Top-p par défaut",
                min_value=0.1,
                max_value=1.0,
                value=0.9,
                step=0.1,
                help="Contrôle la diversité du vocabulaire"
            )
            
            default_presence_penalty = st.slider(
                "Pénalité de présence par défaut",
                min_value=0.0,
                max_value=2.0,
                value=0.1,
                step=0.1,
                help="Évite les répétitions"
            )
        
        if st.button("💾 Sauvegarder les paramètres par défaut"):
            # Sauvegarder dans la session
            st.session_state.default_llm_config = {
                "temperature": default_temperature,
                "max_tokens": default_max_tokens,
                "top_p": default_top_p,
                "presence_penalty": default_presence_penalty
            }
            st.success("✅ Paramètres sauvegardés pour cette session")

def show_file_settings():
    """
    Paramètres de gestion des fichiers.
    """
    st.subheader("📁 Configuration des fichiers")
    
    with st.expander("Paramètres d'upload"):
        # Taille maximale des fichiers
        max_file_size = st.number_input(
            "Taille maximale des fichiers (MB)",
            min_value=1,
            max_value=50,
            value=10,
            help="Taille maximale autorisée pour les fichiers uploadés"
        )
        
        # Formats supportés
        st.markdown("**Formats supportés:**")
        supported_formats = ['PDF', 'TXT', 'DOCX']
        for fmt in supported_formats:
            st.write(f"• {fmt}")
        
        # Dossiers de travail
        st.markdown("**Dossiers de travail:**")
        try:
            from config.settings import Settings
            
            directories = {
                "Upload": Settings.get_upload_path(),
                "Traitement": Settings.get_processed_path(),
                "Export": Settings.get_exports_path()
            }
            
            for name, path in directories.items():
                exists = os.path.exists(path)
                status = "✅" if exists else "❌"
                st.write(f"{status} {name}: `{path}`")
                
        except Exception as e:
            st.error(f"Erreur lors de la vérification des dossiers: {str(e)}")
    
    # Nettoyage des fichiers temporaires
    with st.expander("Nettoyage"):
        st.markdown("""
        Les fichiers temporaires sont automatiquement supprimés après traitement.
        
        Si vous rencontrez des problèmes d'espace disque, vous pouvez nettoyer manuellement les dossiers de travail.
        """)
        
        if st.button("🧹 Nettoyer les fichiers temporaires", type="secondary"):
            try:
                from config.settings import Settings
                import shutil
                
                # Nettoyer les dossiers
                for path in [Settings.get_upload_path(), Settings.get_processed_path()]:
                    if os.path.exists(path):
                        for file in os.listdir(path):
                            file_path = os.path.join(path, file)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                
                st.success("✅ Fichiers temporaires nettoyés")
                
            except Exception as e:
                st.error(f"❌ Erreur lors du nettoyage: {str(e)}")

def show_ui_settings():
    """
    Paramètres de l'interface utilisateur.
    """
    st.subheader("🎨 Interface utilisateur")
    
    with st.expander("Préférences d'affichage"):
        # Thème (note: Streamlit gère cela automatiquement)
        st.markdown("""
        **Thème:** Le thème de l'application suit les paramètres de votre navigateur (clair/sombre).
        """)
        
        # Langue
        language = st.selectbox(
            "Langue de l'interface",
            options=["Français", "English"],
            index=0,
            help="Langue principale de l'interface (redémarrage requis)"
        )
        
        # Affichage des métadonnées
        show_metadata = st.checkbox(
            "Afficher les métadonnées détaillées",
            value=True,
            help="Affiche des informations techniques sur les documents et la génération"
        )
        
        # Mode debug
        debug_mode = st.checkbox(
            "Mode debug",
            value=False,
            help="Affiche des informations de débogage supplémentaires"
        )
        
        if st.button("💾 Sauvegarder les préférences UI"):
            st.session_state.ui_preferences = {
                "language": language,
                "show_metadata": show_metadata,
                "debug_mode": debug_mode
            }
            st.success("✅ Préférences sauvegardées pour cette session")

def show_system_info():
    """
    Informations système et diagnostics.
    """
    st.subheader("🔧 Informations système")
    
    with st.expander("Statut des composants", expanded=True):
        try:
            from core.services.document_service import DocumentService
            
            # Test du service
            with st.spinner("Vérification du statut..."):
                service = DocumentService()
                status = service.get_service_status()
            
            # Affichage du statut
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Service principal:**")
                if status.get('service_initialized', False):
                    st.success("✅ Service initialisé")
                else:
                    st.error("❌ Service non initialisé")
                
                st.markdown("**Connexion LLM:**")
                if status.get('llm_connection', False):
                    st.success("✅ Connexion opérationnelle")
                else:
                    st.error("❌ Connexion échouée")
            
            with col2:
                st.markdown("**Dossiers:**")
                directories = status.get('directories_ready', {})
                for name, ready in directories.items():
                    if ready:
                        st.success(f"✅ {name.capitalize()}")
                    else:
                        st.error(f"❌ {name.capitalize()}")
            
            # Informations détaillées
            if st.checkbox("Afficher les détails techniques"):
                st.json(status)
                
        except Exception as e:
            st.error(f"❌ Erreur lors de la vérification du statut: {str(e)}")
    
    with st.expander("Versions et dépendances"):
        st.markdown("""
        **InspireDoc** - Version 1.0.0 (MVP)
        
        **Dépendances principales:**
        - Streamlit (Interface utilisateur)
        - OpenAI/Azure OpenAI (Modèle de langage)
        - python-docx (Traitement DOCX)
        - pypdf/pdfplumber (Traitement PDF)
        - weasyprint/pdfkit (Export PDF)
        - markdown (Rendu Markdown)
        """)
        
        # Test des imports
        if st.button("🔍 Vérifier les dépendances"):
            dependencies = {
                "streamlit": "streamlit",
                "requests": "requests",
                "python-docx": "docx",
                "pypdf": "pypdf",
                "pdfplumber": "pdfplumber",
                "weasyprint": "weasyprint",
                "pdfkit": "pdfkit",
                "markdown": "markdown",
                "chardet": "chardet"
            }
            
            for name, module in dependencies.items():
                try:
                    __import__(module)
                    st.success(f"✅ {name}")
                except ImportError:
                    st.error(f"❌ {name} - Non installé")
    
    # Actions de maintenance
    with st.expander("Actions de maintenance"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Redémarrer le service"):
                try:
                    # Réinitialiser le service dans la session
                    if 'document_service' in st.session_state:
                        del st.session_state.document_service
                    st.success("✅ Service redémarré (rechargez la page)")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
        
        with col2:
            if st.button("🗑️ Vider le cache"):
                try:
                    # Vider le cache Streamlit
                    st.cache_data.clear()
                    st.success("✅ Cache vidé")
                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")