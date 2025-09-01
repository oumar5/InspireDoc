import streamlit as st
from datetime import datetime

def show_about_interface():
    """
    Interface de la page À propos.
    """
    # CSS adaptatif pour le mode sombre/clair
    st.markdown("""
    <style>
    .feature-card {
        background-color: var(--background-color-secondary, #f8f9fa);
        color: var(--text-color, #2c3e50);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color, #3498db);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card h4 {
        color: var(--text-color, #2c3e50);
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: var(--text-color-secondary, #34495e);
        margin-bottom: 0;
    }
    
    /* Thème sombre */
    @media (prefers-color-scheme: dark) {
        .feature-card {
            background-color: var(--background-color-secondary, #2d3748);
            color: var(--text-color, #ffffff);
        }
        .feature-card h4 {
            color: var(--text-color, #ffffff);
        }
        .feature-card p {
            color: var(--text-color-secondary, #b0b0b0);
        }
    }
    
    /* Adaptation Streamlit thème sombre */
    [data-theme="dark"] .feature-card {
        background-color: #2d3748;
        color: #ffffff;
    }
    
    [data-theme="dark"] .feature-card h4 {
        color: #ffffff;
    }
    
    [data-theme="dark"] .feature-card p {
        color: #b0b0b0;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    InspireDoc est une application web révolutionnaire qui utilise l'**architecture 3+1** et l'intelligence 
    artificielle pour générer automatiquement des documents en analysant et appliquant des transformations intelligentes.
    
    ### 🎯 Innovation : Architecture 3+1
    
    InspireDoc révolutionne la génération de documents avec son approche unique :
    
    1. **📜 Document source ancien** - Référence originale
    2. **🎨 Document exemple construit** - Transformation appliquée sur la source
    3. **📄 Nouveau document source** - Nouvelle information à traiter
    4. **💬 Description utilisateur** - Instructions personnalisées (optionnel)
    
    ### 🧠 Intelligence de transformation
    
    L'IA **analyse** comment le document ancien a été transformé en exemple, puis **applique** 
    cette même transformation sur vos nouveaux documents sources.
    """)
    
    # Statistiques du projet
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Version", "2.0.0 Architecture 3+1")
    with col2:
        st.metric("Formats supportés", "3 (PDF, TXT, DOCX)")
    with col3:
        st.metric("Intelligence", "Transformation IA")
    with col4:
        st.metric("Thèmes", "Sombre/Clair adaptatif")

def show_features():
    """
    Présentation des fonctionnalités.
    """
    st.subheader("🚀 Fonctionnalités principales")
    
    features = [
        {
            "icon": "🧠",
            "title": "Architecture 3+1 révolutionnaire",
            "description": "Analyse les transformations et les applique intelligemment sur de nouveaux documents"
        },
        {
            "icon": "📄",
            "title": "Upload intelligent 3 zones",
            "description": "Source ancien, exemple construit, nouveau source + description optionnelle"
        },
        {
            "icon": "🔄",
            "title": "Transformation contextuelle",
            "description": "L'IA comprend COMMENT transformer, pas seulement QUOI transformer"
        },
        {
            "icon": "🎨",
            "title": "Rendu Markdown amélioré",
            "description": "Styles adaptatifs, thèmes sombre/clair, rendu professionnel"
        },
        {
            "icon": "📥",
            "title": "Export multi-format",
            "description": "PDF et DOCX avec préservation complète des styles et mise en forme"
        },
        {
            "icon": "🐳",
            "title": "Docker & Hot Reload",
            "description": "Développement containerisé avec rechargement automatique des modifications"
        }
    ]
    
    # Affichage en grille
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(features):
                feature = features[i]
                st.markdown(f"""
                <div class="feature-card">
                    <h4>{feature['icon']} {feature['title']}</h4>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(features):
                feature = features[i + 1]
                st.markdown(f"""
                <div class="feature-card">
                    <h4>{feature['icon']} {feature['title']}</h4>
                    <p>{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)

def show_technical_info():
    """
    Informations techniques sur l'architecture.
    """
    st.subheader("🔧 Architecture technique")
    
    with st.expander("🧠 Innovation : Architecture 3+1", expanded=True):
        st.markdown("""
        ### Révolution dans la génération de documents
        
        **Méthodologie unique :**
        1. **ANALYSER** : Comprendre la transformation (Ancien → Exemple)
        2. **IDENTIFIER** : Repérer les patterns (style, structure, ton, format)
        3. **APPLIQUER** : Utiliser ces patterns sur le nouveau document
        4. **GÉNÉRER** : Créer un résultat cohérent suivant la transformation
        
        **Avantages :**
        - ✅ L'IA comprend le **COMMENT** transformer, pas seulement le **QUOI**
        - ✅ Génération contextuelle et intelligente
        - ✅ Respect fidèle des patterns de transformation
        - ✅ Personnalisation via description utilisateur
        """)
    
    with st.expander("Stack technologique", expanded=False):
        st.markdown("""
        ### Langage et Framework
        - **Python 3.10+** - Langage principal
        - **Streamlit** - Interface utilisateur web moderne
        - **Docker** - Containerisation et déploiement
        
        ### Traitement de documents
        - **pypdf/pdfplumber** - Extraction PDF intelligente
        - **python-docx** - Traitement DOCX complet
        - **chardet** - Détection d'encodage automatique
        
        ### Intelligence Artificielle
        - **OpenAI GPT-4o** - Modèle de langage avancé
        - **Azure OpenAI** - Service cloud sécurisé
        - **Architecture 3+1** - Innovation InspireDoc
        
        ### Interface et Rendu
        - **CSS adaptatif** - Thèmes sombre/clair automatiques
        - **Markdown enrichi** - Rendu professionnel
        - **Hot reload** - Développement optimisé
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
    
    with st.expander("🚀 Workflow Architecture 3+1", expanded=True):
        st.markdown("""
        ### Nouveau workflow révolutionnaire
        
        **1. 📜 Document source ancien**
        - Uploadez votre document de référence original
        - Exemple : Un rapport technique existant
        
        **2. 🎨 Document exemple construit**
        - Uploadez un exemple créé à partir de la source
        - Exemple : Le même rapport transformé en présentation
        
        **3. 📄 Nouveau document source**
        - Uploadez le nouveau contenu à traiter
        - Exemple : Un nouveau rapport technique à transformer
        
        **4. 💬 Description optionnelle**
        - Ajoutez des instructions personnalisées
        - Exemple : "Adapter le ton pour un public jeune"
        
        **5. 🧠 Génération intelligente**
        - L'IA analyse la transformation (ancien → exemple)
        - Applique la même transformation (nouveau → résultat)
        - Génère un document cohérent et professionnel
        
        **6. 📖 Rendu et export**
        - Prévisualisez avec rendu Markdown amélioré
        - Exportez en PDF ou DOCX avec styles préservés
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
        st.info(f"**Version:** 2.0.0 Architecture 3+1")
    
    with col2:
        st.info(f"**Dernière mise à jour:** {datetime.now().strftime('%B %Y')}")
    
    with col3:
        st.info(f"**Statut:** Production Ready")
    
    # Innovation et remerciements
    st.markdown("""
    ### 🚀 Innovation InspireDoc
    
    **Architecture 3+1 révolutionnaire :**
    - Première implémentation de transformation contextuelle intelligente
    - L'IA comprend le **COMMENT** transformer, pas seulement le **QUOI**
    - Génération basée sur l'analyse de patterns de transformation
    - Interface adaptative avec thèmes sombre/clair automatiques
    
    ### 🙏 Remerciements
    
    Merci aux technologies qui ont rendu cette innovation possible :
    - **Streamlit** pour l'interface utilisateur moderne
    - **OpenAI GPT-4o** pour l'intelligence artificielle avancée
    - **Docker** pour la containerisation et le déploiement
    - **Python** et son écosystème riche pour le développement rapide
    """)
    
    # Contact et support
    with st.expander("📞 Support et contact"):
        st.markdown("""
        ### Support technique
        
        Pour toute question ou problème technique :
        
        1. **Vérifiez d'abord** la page Paramètres pour le statut du système
        2. **Consultez** la section Résolution de problèmes ci-dessus
        3. **Vérifiez** que toutes les dépendances sont installées
        
        ### Évolutions futures
        
        InspireDoc 2.0 avec Architecture 3+1 ouvre de nouvelles possibilités :
        - **Formats étendus** : Support d'images, tableaux complexes
        - **IA multimodale** : Analyse de documents avec images
        - **Templates intelligents** : Bibliothèque de transformations pré-définies
        - **Collaboration** : Partage et versioning des transformations
        - **API REST** : Intégration dans d'autres applications
        - **Analytics** : Métriques sur l'efficacité des transformations
        - API REST
        
        N'hésitez pas à contribuer ou suggérer des améliorations !
        """)