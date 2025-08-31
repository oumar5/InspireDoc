import streamlit as st
import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au path pour les imports
sys.path.append(str(Path(__file__).parent))

# Configuration de la page
st.set_page_config(
    page_title="InspireDoc",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #34495e;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .feature-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """
    Application principale InspireDoc.
    """
    
    # En-tête principal
    st.markdown('<h1 class="main-header">📝 InspireDoc</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Générateur intelligent de documents basé sur l\'IA</p>', unsafe_allow_html=True)
    
    # Sidebar pour la navigation
    with st.sidebar:
        st.title("Navigation")
        
        # Menu de navigation
        page = st.selectbox(
            "Choisir une page",
            ["🏠 Accueil", "⚡ Génération", "⚙️ Paramètres", "ℹ️ À propos"]
        )
    
    # Routage des pages
    if page == "🏠 Accueil":
        show_home_page()
    elif page == "⚡ Génération":
        show_generation_page()
    elif page == "⚙️ Paramètres":
        show_settings_page()
    elif page == "ℹ️ À propos":
        show_about_page()

def show_home_page():
    """
    Page d'accueil.
    """
    st.header("Bienvenue sur InspireDoc")
    
    # Description
    st.markdown("""
    InspireDoc est un outil intelligent qui vous permet de générer automatiquement des documents 
    en vous inspirant d'exemples existants et en utilisant vos documents sources.
    """)
    
    # Fonctionnalités principales
    st.subheader("🚀 Fonctionnalités principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>📄 Upload de documents</h4>
            <p>Supporté: PDF, TXT, DOCX</p>
            <ul>
                <li>Documents sources (contenu)</li>
                <li>Documents exemples (style)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🤖 Génération IA</h4>
            <p>Utilise GPT-4o pour générer des documents intelligents</p>
            <ul>
                <li>Respect du style des exemples</li>
                <li>Contenu basé sur les sources</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🎨 Rendu Markdown</h4>
            <p>Affichage élégant et professionnel</p>
            <ul>
                <li>Prévisualisation en temps réel</li>
                <li>Mise en forme préservée</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>📥 Export multi-format</h4>
            <p>Exportez vos documents générés</p>
            <ul>
                <li>PDF avec styles personnalisés</li>
                <li>DOCX compatible Office</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Guide de démarrage rapide
    st.subheader("🎯 Démarrage rapide")
    
    st.markdown("""
    1. **Préparez vos documents** : Rassemblez vos documents sources (contenu) et exemples (style)
    2. **Allez à la page Génération** : Utilisez le menu de navigation
    3. **Uploadez vos fichiers** : Glissez-déposez ou sélectionnez vos documents
    4. **Décrivez votre demande** : Expliquez quel type de document vous voulez générer
    5. **Générez et exportez** : Laissez l'IA créer votre document et exportez-le
    """)
    
    # Statut du système
    st.subheader("🔧 Statut du système")
    
    try:
        from core.services.document_service import DocumentService
        service = DocumentService()
        status = service.get_service_status()
        
        if status.get('service_initialized', False):
            st.markdown('<div class="success-box">✅ Service InspireDoc initialisé avec succès</div>', unsafe_allow_html=True)
            
            if status.get('llm_connection', False):
                st.markdown('<div class="success-box">✅ Connexion LLM opérationnelle</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-box">❌ Problème de connexion LLM</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ Erreur d\'initialisation du service</div>', unsafe_allow_html=True)
            if 'error' in status:
                st.error(f"Erreur: {status['error']}")
    
    except Exception as e:
        st.markdown('<div class="error-box">❌ Impossible de vérifier le statut du système</div>', unsafe_allow_html=True)
        st.error(f"Erreur: {str(e)}")
        st.markdown("""
        <div class="info-box">
            <strong>Configuration requise:</strong><br>
            Assurez-vous que les variables d'environnement suivantes sont définies:
            <ul>
                <li><code>GPT4O_API_KEY</code> - Votre clé API GPT-4o</li>
                <li><code>GPT4O_ENDPOINT</code> - L'endpoint de votre service GPT-4o</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_generation_page():
    """
    Page de génération de documents.
    """
    try:
        from pages.generation import show_generation_interface
        show_generation_interface()
    except ImportError as e:
        st.error(f"Erreur d'import de la page de génération: {str(e)}")
        st.info("La page de génération sera bientôt disponible.")

def show_settings_page():
    """
    Page des paramètres.
    """
    try:
        from pages.settings import show_settings_interface
        show_settings_interface()
    except ImportError as e:
        st.error(f"Erreur d'import de la page des paramètres: {str(e)}")
        st.info("La page des paramètres sera bientôt disponible.")

def show_about_page():
    """
    Page à propos.
    """
    try:
        from pages.about import show_about_interface
        show_about_interface()
    except ImportError as e:
        st.error(f"Erreur d'import de la page à propos: {str(e)}")
        st.info("La page à propos sera bientôt disponible.")

if __name__ == "__main__":
    main()