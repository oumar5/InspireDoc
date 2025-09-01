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
    /* Masquer la navigation par défaut de Streamlit */
    .css-1d391kg {display: none;}
    .css-1rs6os {display: none;}
    .css-17ziqus {display: none;}
    .css-1v0mbdj {display: none;}
    .css-1wbqy5l {display: none;}
    .stSelectbox > div > div > div {display: none;}
    
    /* Masquer les éléments de navigation automatique */
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        display: none;
    }
    
    /* Adaptation automatique aux thèmes sombre/clair */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: var(--text-color, #2c3e50);
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: var(--text-color-secondary, #34495e);
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .feature-box {
        background-color: var(--background-color-secondary, #f8f9fa);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color, #3498db);
        margin: 1rem 0;
        color: var(--text-color, #2c3e50);
    }
    
    .success-box {
        background-color: var(--success-bg, #d4edda);
        border: 1px solid var(--success-border, #c3e6cb);
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--success-text, #155724);
    }
    
    .error-box {
        background-color: var(--error-bg, #f8d7da);
        border: 1px solid var(--error-border, #f5c6cb);
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--error-text, #721c24);
    }
    
    .info-box {
        background-color: var(--info-bg, #d1ecf1);
        border: 1px solid var(--info-border, #bee5eb);
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: var(--info-text, #0c5460);
    }
    
    /* Thème sombre */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #ffffff;
            --text-color-secondary: #b0b0b0;
            --background-color-secondary: #2d3748;
            --primary-color: #4299e1;
            --success-bg: #2d5a3d;
            --success-border: #4a7c59;
            --success-text: #9ae6b4;
            --error-bg: #5a2d2d;
            --error-border: #7c4a4a;
            --error-text: #feb2b2;
            --info-bg: #2d4a5a;
            --info-border: #4a6c7c;
            --info-text: #90cdf4;
        }
    }
    
    /* Thème clair */
    @media (prefers-color-scheme: light) {
        :root {
            --text-color: #2c3e50;
            --text-color-secondary: #34495e;
            --background-color-secondary: #f8f9fa;
            --primary-color: #3498db;
            --success-bg: #d4edda;
            --success-border: #c3e6cb;
            --success-text: #155724;
            --error-bg: #f8d7da;
            --error-border: #f5c6cb;
            --error-text: #721c24;
            --info-bg: #d1ecf1;
            --info-border: #bee5eb;
            --info-text: #0c5460;
        }
    }
    
    /* Adaptation Streamlit thème sombre */
    [data-theme="dark"] {
        --text-color: #ffffff;
        --text-color-secondary: #b0b0b0;
        --background-color-secondary: #2d3748;
        --primary-color: #4299e1;
        --success-bg: #2d5a3d;
        --success-border: #4a7c59;
        --success-text: #9ae6b4;
        --error-bg: #5a2d2d;
        --error-border: #7c4a4a;
        --error-text: #feb2b2;
        --info-bg: #2d4a5a;
        --info-border: #4a6c7c;
        --info-text: #90cdf4;
    }
    
    /* Adaptation Streamlit thème clair */
    [data-theme="light"] {
        --text-color: #2c3e50;
        --text-color-secondary: #34495e;
        --background-color-secondary: #f8f9fa;
        --primary-color: #3498db;
        --success-bg: #d4edda;
        --success-border: #c3e6cb;
        --success-text: #155724;
        --error-bg: #f8d7da;
        --error-border: #f5c6cb;
        --error-text: #721c24;
        --info-bg: #d1ecf1;
        --info-border: #bee5eb;
        --info-text: #0c5460;
    }
    
    /* Amélioration du rendu Markdown */
    .markdown-content {
        line-height: 1.6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .markdown-content h1, .markdown-content h2, .markdown-content h3 {
        color: var(--text-color, #2c3e50);
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .markdown-content h1 {
        font-size: 2rem;
        border-bottom: 2px solid var(--primary-color, #3498db);
        padding-bottom: 0.3rem;
    }
    
    .markdown-content h2 {
        font-size: 1.5rem;
        border-bottom: 1px solid var(--text-color-secondary, #34495e);
        padding-bottom: 0.2rem;
    }
    
    .markdown-content h3 {
        font-size: 1.25rem;
    }
    
    .markdown-content p {
        margin-bottom: 1rem;
        text-align: justify;
    }
    
    .markdown-content ul, .markdown-content ol {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .markdown-content li {
        margin-bottom: 0.25rem;
    }
    
    .markdown-content blockquote {
        border-left: 4px solid var(--primary-color, #3498db);
        margin: 1rem 0;
        padding-left: 1rem;
        font-style: italic;
        background-color: var(--background-color-secondary, #f8f9fa);
        padding: 0.5rem 1rem;
    }
    
    .markdown-content code {
        background-color: var(--background-color-secondary, #f8f9fa);
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
    }
    
    .markdown-content pre {
        background-color: var(--background-color-secondary, #f8f9fa);
        padding: 1rem;
        border-radius: 5px;
        overflow-x: auto;
        margin: 1rem 0;
    }
    
    .markdown-content table {
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
    }
    
    .markdown-content th, .markdown-content td {
        border: 1px solid var(--text-color-secondary, #34495e);
        padding: 0.5rem;
        text-align: left;
    }
    
    .markdown-content th {
        background-color: var(--primary-color, #3498db);
        color: white;
        font-weight: bold;
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
    from components.sidebar import show_sidebar
    page = show_sidebar()
    
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
    st.header("🚀 Bienvenue sur InspireDoc 2.0")
    
    # Description révolutionnaire
    st.markdown("""
    ## 🧠 Architecture 3+1 Révolutionnaire
    
    InspireDoc révolutionne la génération de documents avec son **intelligence de transformation**. 
    L'IA ne se contente plus de copier - elle **comprend** et **applique** des transformations intelligentes.
    
    ### 💡 Innovation unique :
    L'IA analyse comment un document ancien a été transformé en exemple, puis applique cette même transformation sur vos nouveaux documents.
    """)
    
    # Workflow 3+1
    st.markdown("""
    ### 🔄 Workflow Architecture 3+1
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>📜 1. Source Ancien</h4>
            <p>Document de référence original</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🎨 2. Exemple Construit</h4>
            <p>Transformation appliquée</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box">
            <h4>📄 3. Nouveau Source</h4>
            <p>Information à traiter</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-box">
            <h4>💬 4. Description</h4>
            <p>Instructions optionnelles</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Fonctionnalités révolutionnaires
    st.subheader("✨ Fonctionnalités révolutionnaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4>🧠 Intelligence de Transformation</h4>
            <p>L'IA comprend le COMMENT transformer, pas seulement le QUOI</p>
            <ul>
                <li>Analyse des patterns de transformation</li>
                <li>Application contextuelle intelligente</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>📄 Upload Intelligent 3 Zones</h4>
            <p>Architecture 3+1 révolutionnaire</p>
            <ul>
                <li>Source ancien + Exemple construit + Nouveau source</li>
                <li>Description utilisateur optionnelle</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4>🎨 Rendu Adaptatif</h4>
            <p>Interface qui s'adapte automatiquement</p>
            <ul>
                <li>Thèmes sombre/clair automatiques</li>
                <li>Rendu Markdown professionnel</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-box">
            <h4>🐳 Docker & Hot Reload</h4>
            <p>Développement et déploiement optimisés</p>
            <ul>
                <li>Containerisation complète</li>
                <li>Rechargement automatique</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Guide Architecture 3+1
    st.subheader("🎯 Guide Architecture 3+1")
    
    st.markdown("""
    ### 🚀 Nouveau workflow révolutionnaire :
    
    1. **📜 Document source ancien** : Uploadez votre document de référence original
    2. **🎨 Document exemple construit** : Uploadez un exemple créé à partir de la source
    3. **📄 Nouveau document source** : Uploadez le nouveau contenu à traiter
    4. **💬 Description optionnelle** : Ajoutez des instructions personnalisées
    5. **🧠 Génération intelligente** : L'IA analyse la transformation et l'applique
    6. **📖 Rendu et export** : Prévisualisez et exportez en PDF/DOCX
    
    ### 💡 Exemple concret :
    - **Ancien** : Rapport technique brut
    - **Exemple** : Le même rapport transformé en présentation
    - **Nouveau** : Nouveau rapport technique à transformer
    - **Résultat** : Nouvelle présentation avec le même style !
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
        from modules.generation import show_generation_interface
        show_generation_interface()
    except ImportError as e:
        st.error(f"Erreur d'import de la page de génération: {str(e)}")
        st.info("La page de génération sera bientôt disponible.")

def show_settings_page():
    """
    Page des paramètres.
    """
    try:
        from modules.settings import show_settings_interface
        show_settings_interface()
    except ImportError as e:
        st.error(f"Erreur d'import de la page des paramètres: {str(e)}")
        st.info("La page des paramètres sera bientôt disponible.")

def show_about_page():
    """
    Page à propos.
    """
    try:
        from modules.about import show_about_interface
        show_about_interface()
    except ImportError as e:
        st.error(f"Erreur d'import de la page à propos: {str(e)}")
        st.info("La page à propos sera bientôt disponible.")

if __name__ == "__main__":
    main()