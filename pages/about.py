import streamlit as st
from datetime import datetime

def show_about_interface():
    """
    Interface de la page À propos.
    """
    st.header("ℹ️ À propos d'InspireDoc")
    
    # Présentation principale
    show_main_presentation()
    
    # Fonctionnalités
    show_features()
    
    # Architecture technique
    show_technical_info()
    
    # Guide d'utilisation
    show_usage_guide()
    
    # Crédits et licence
    show_credits()

def show_main_presentation():
    """
    Présentation principale du projet.
    """
    st.markdown("""
    ## 📝 InspireDoc - Générateur intelligent de documents
    
    InspireDoc est une application web innovante qui utilise l'intelligence artificielle pour générer 
    automatiquement des documents en s'inspirant d'exemples existants et en utilisant vos documents sources.
    
    ### 🎯 Objectif
    
    Simplifier et automatiser la création de documents professionnels en combinant :
    - **Le contenu** de vos documents sources
    - **Le style et la structure** de vos documents exemples
    - **La puissance de l'IA** pour une génération intelligente
    """)
    
    # Statistiques du projet
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Version", "1.0.0 MVP")
    with col2:
        st.metric("Formats supportés", "3")
    with col3:
        st.metric("Modules", "10+")
    with col4:
        st.metric("Développement", "2024")

def show_features():
    """
    Présentation des fonctionnalités.
    """
    st.subheader("🚀 Fonctionnalités principales")
    
    features = [
        {
            "icon": "📄",
            "title": "Upload multi-format",
            "description": "Supporté: PDF, TXT, DOCX avec extraction intelligente du contenu"
        },
        {
            "icon": "🧹",
            "title": "Nettoyage automatique",
            "description": "Suppression des métadonnées, normalisation du texte, optimisation pour l'IA"
        },
        {
            "icon": "🤖",
            "title": "Génération IA",
            "description": "Utilise GPT-4o pour créer des documents respectant style et contenu"
        },
        {
            "icon": "🎨",
            "title": "Rendu Markdown",
            "description": "Affichage élégant avec prévisualisation en temps réel"
        },
        {
            "icon": "📥",
            "title": "Export multi-format",
            "description": "Export en PDF et DOCX avec préservation de la mise en forme"
        },
        {
            "icon": "⚙️",
            "title": "Configuration avancée",
            "description": "Paramètres personnalisables pour la génération et l'interface"
        }
    ]
    
    # Affichage en grille
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(features):
                feature = features[i]
                st.markdown(f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 1.5rem;
                    border-radius: 10px;
                    border-left: 4px solid #3498db;
                    margin: 1rem 0;
                ">
                    <h4>{feature['icon']} {feature['title']}</h4>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(features):
                feature = features[i + 1]
                st.markdown(f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 1.5rem;
                    border-radius: 10px;
                    border-left: 4px solid #3498db;
                    margin: 1rem 0;
                ">
                    <h4>{feature['icon']} {feature['title']}</h4>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)

def show_technical_info():
    """
    Informations techniques sur l'architecture.
    """
    st.subheader("🔧 Architecture technique")
    
    with st.expander("Stack technologique", expanded=False):
        st.markdown("""
        ### Langage et Framework
        - **Python 3.10+** - Langage principal
        - **Streamlit** - Interface utilisateur web
        
        ### Traitement de documents
        - **pypdf/pdfplumber** - Extraction PDF
        - **python-docx** - Traitement DOCX
        - **chardet** - Détection d'encodage
        
        ### Intelligence Artificielle
        - **OpenAI GPT-4o** - Modèle de langage
        - **Azure OpenAI** - Service cloud
        
        ### Rendu et Export
        - **markdown** - Traitement Markdown
        - **weasyprint/pdfkit** - Export PDF
        - **python-docx** - Export DOCX
        """)
    
    with st.expander("Architecture modulaire", expanded=False):
        st.markdown("""
        ### Structure du projet
        
        ```
        inspiredoc/
        ├── app.py                    # Application principale
        ├── config/
        │   └── settings.py          # Configuration centralisée
        ├── core/
        │   ├── ingestion/           # Chargement des documents
        │   ├── preprocessing/       # Nettoyage et normalisation
        │   ├── llm/                # Interaction avec l'IA
        │   ├── rendering/          # Export PDF/DOCX
        │   ├── services/           # Services métier
        │   └── utils/              # Utilitaires
        ├── pages/                  # Pages Streamlit
        └── data/                   # Données temporaires
        ```
        
        ### Principes de conception
        - **Séparation des responsabilités** - Chaque module a un rôle spécifique
        - **Modularité** - Composants réutilisables et testables
        - **Extensibilité** - Facilité d'ajout de nouvelles fonctionnalités
        - **Robustesse** - Gestion d'erreurs et logging complet
        """)

def show_usage_guide():
    """
    Guide d'utilisation détaillé.
    """
    st.subheader("📖 Guide d'utilisation")
    
    with st.expander("Démarrage rapide", expanded=True):
        st.markdown("""
        ### 1. Configuration initiale
        
        Avant d'utiliser InspireDoc, configurez vos variables d'environnement :
        
        ```bash
        export GPT4O_API_KEY="votre_cle_api_gpt4o"
        export GPT4O_ENDPOINT="https://votre-endpoint.openai.azure.com"
        ```
        
        ### 2. Préparation des documents
        
        - **Documents sources** : Contiennent les informations à utiliser
        - **Documents exemples** : Définissent le style et la structure souhaités
        - **Formats acceptés** : PDF, TXT, DOCX (max 10 MB)
        
        ### 3. Génération
        
        1. Uploadez vos documents dans la page Génération
        2. Décrivez précisément le document souhaité
        3. Ajustez les paramètres si nécessaire
        4. Lancez la génération
        5. Prévisualisez et exportez le résultat
        """)
    
    with st.expander("Conseils d'utilisation", expanded=False):
        st.markdown("""
        ### 💡 Conseils pour de meilleurs résultats
        
        **Choix des documents sources :**
        - Utilisez des documents avec un contenu riche et structuré
        - Évitez les documents avec trop de métadonnées ou de bruit
        - Préférez des textes dans la même langue que le document final
        
        **Choix des documents exemples :**
        - Sélectionnez des documents avec la structure souhaitée
        - Assurez-vous que le style correspond à vos attentes
        - Utilisez des exemples de qualité professionnelle
        
        **Rédaction de la demande :**
        - Soyez précis sur le type de document souhaité
        - Mentionnez le ton et le style (formel, technique, etc.)
        - Spécifiez la longueur approximative si importante
        - Indiquez les éléments clés à inclure ou exclure
        
        **Paramètres de génération :**
        - **Température basse (0.1-0.3)** : Plus conservateur, suit mieux les exemples
        - **Température élevée (0.7-0.9)** : Plus créatif, peut s'éloigner des exemples
        - **Tokens élevés** : Pour des documents plus longs
        - **Présence penalty** : Pour éviter les répétitions
        """)
    
    with st.expander("Résolution de problèmes", expanded=False):
        st.markdown("""
        ### 🔧 Problèmes courants
        
        **Erreur de connexion LLM :**
        - Vérifiez vos variables d'environnement
        - Testez votre clé API et endpoint
        - Vérifiez votre connexion internet
        
        **Fichier non traité :**
        - Vérifiez le format (PDF, TXT, DOCX uniquement)
        - Contrôlez la taille (max 10 MB)
        - Assurez-vous que le fichier n'est pas corrompu
        
        **Génération de mauvaise qualité :**
        - Améliorez la description de votre demande
        - Utilisez des documents exemples plus clairs
        - Ajustez les paramètres de température
        - Vérifiez que vos documents sources sont pertinents
        
        **Export PDF/DOCX échoue :**
        - Installez les dépendances manquantes (weasyprint, pdfkit)
        - Vérifiez les permissions d'écriture
        - Essayez avec un document plus court
        """)

def show_credits():
    """
    Crédits et informations légales.
    """
    st.subheader("👥 Crédits et licence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏗️ Développement
        
        **InspireDoc** a été développé comme un MVP (Minimum Viable Product) 
        pour démontrer les capacités de génération automatique de documents 
        basée sur l'intelligence artificielle.
        
        **Technologies utilisées :**
        - OpenAI GPT-4o pour la génération
        - Streamlit pour l'interface
        - Python pour le backend
        """)
    
    with col2:
        st.markdown("""
        ### 📄 Licence et utilisation
        
        Ce projet est développé à des fins de démonstration et d'apprentissage.
        
        **Avertissements :**
        - Vérifiez toujours le contenu généré
        - Respectez les conditions d'utilisation d'OpenAI
        - Protégez vos documents confidentiels
        - Sauvegardez vos données importantes
        """)
    
    # Informations de version
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Version:** 1.0.0 MVP")
    
    with col2:
        st.info(f"**Dernière mise à jour:** {datetime.now().strftime('%B %Y')}")
    
    with col3:
        st.info(f"**Statut:** Démonstration")
    
    # Remerciements
    st.markdown("""
    ### 🙏 Remerciements
    
    Merci à toutes les technologies open source qui ont rendu ce projet possible :
    - **Streamlit** pour l'interface utilisateur intuitive
    - **OpenAI** pour les capacités d'IA avancées
    - **Python** et son écosystème riche
    - La communauté des développeurs pour les nombreuses bibliothèques utilisées
    """)
    
    # Contact et support
    with st.expander("📞 Support et contact"):
        st.markdown("""
        ### Support technique
        
        Pour toute question ou problème technique :
        
        1. **Vérifiez d'abord** la page Paramètres pour le statut du système
        2. **Consultez** la section Résolution de problèmes ci-dessus
        3. **Vérifiez** que toutes les dépendances sont installées
        
        ### Améliorations et suggestions
        
        Ce projet étant un MVP, de nombreuses améliorations sont possibles :
        - Support de formats additionnels
        - Interface multilingue
        - Gestion de projets
        - Base de données vectorielle
        - Authentification utilisateur
        - API REST
        
        N'hésitez pas à contribuer ou suggérer des améliorations !
        """)