import streamlit as st
import os
import tempfile
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Configuration du logger
logger = logging.getLogger(__name__)

# Imports InspireDoc
try:
    from core.services.document_service import DocumentService
    from core.rendering.markdown_to_pdf import MarkdownToPDFConverter
    from core.rendering.markdown_to_docx import MarkdownToDOCXConverter
    from config.settings import Settings
except ImportError as e:
    st.error(f"Erreur d'import des modules InspireDoc: {str(e)}")
    st.stop()

def show_generation_interface():
    """
    Interface principale de génération de documents.
    """
    st.header("⚡ Génération de documents")
    
    # Initialisation du service
    if 'document_service' not in st.session_state:
        try:
            st.session_state.document_service = DocumentService()
            st.success("✅ Service InspireDoc initialisé")
        except Exception as e:
            st.error(f"❌ Erreur d'initialisation: {str(e)}")
            st.info("Vérifiez que les variables d'environnement GPT4O_API_KEY et GPT4O_ENDPOINT sont définies.")
            return
    
    # Interface d'upload
    show_upload_section()
    
    # Interface de génération
    if st.session_state.get('files_processed', False):
        show_generation_section()
    
    # Interface de résultats
    if st.session_state.get('document_generated', False):
        show_results_section()

def show_upload_section():
    """
    Section d'upload des fichiers.
    """
    st.subheader("📁 Upload des documents")
    
    # Instructions
    with st.expander("ℹ️ Instructions d'utilisation", expanded=False):
        st.markdown("""
        **Architecture 3+1 documents** :
        
        1. **Document source ancien** : Document de référence original
        2. **Document exemple construit** : Exemple créé à partir de la source (montre la transformation souhaitée)
        3. **Nouveau document source** : Nouvelle information à traiter avec la même transformation
        4. **Description optionnelle** : Prompt personnalisé pour affiner la génération
        
        **Formats supportés** : PDF, TXT, DOCX (max 10 MB par fichier)
        """)
    
    # Layout en 3 colonnes pour les 3 documents
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📜 Document source ancien**")
        old_source_files = st.file_uploader(
            "Document de référence original",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            key="old_source_files",
            help="Document original servant de base de référence"
        )
    
    with col2:
        st.markdown("**🎨 Document exemple construit**")
        example_files = st.file_uploader(
            "Exemple créé à partir de la source",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            key="example_files",
            help="Exemple montrant la transformation souhaitée (ancien → exemple)"
        )
    
    with col3:
        st.markdown("**📄 Nouveau document source**")
        new_source_files = st.file_uploader(
            "Nouvelle information à traiter",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            key="new_source_files",
            help="Nouveau contenu qui subira la même transformation"
        )
    
    # Zone de description optionnelle
    st.markdown("**💬 Description personnalisée (optionnel)**")
    user_description = st.text_area(
        "Décrivez le type de document souhaité ou des instructions spécifiques",
        placeholder="Ex: Créer un rapport technique, adapter le ton pour un public jeune, ajouter des exemples pratiques...",
        height=100,
        key="user_description",
        help="Cette description permettra d'affiner la génération selon vos besoins spécifiques"
    )
    
    # Bouton de traitement
    if st.button("🔄 Traiter les fichiers", type="primary"):
        if not old_source_files and not example_files and not new_source_files:
            st.error("Veuillez uploader au moins un document dans chaque catégorie pour la génération.")
            return
        
        if not old_source_files or not example_files or not new_source_files:
            st.warning("⚠️ Pour une génération optimale, il est recommandé d'avoir les 3 types de documents.")
            if not st.button("Continuer quand même", key="continue_anyway"):
                return
        
        with st.spinner("Traitement des fichiers en cours..."):
            try:
                logger.info(f"Début du traitement des fichiers - Anciens: {len(old_source_files or [])}, Exemples: {len(example_files or [])}, Nouveaux: {len(new_source_files or [])}")
                
                # Traitement des fichiers avec la nouvelle architecture 3+1
                processed_old_sources, processed_examples, processed_new_sources = st.session_state.document_service.process_uploaded_files(
                    old_source_files or [],
                    example_files or [],
                    new_source_files or []
                )
                
                logger.info(f"Fichiers traités avec succès - Anciens: {len(processed_old_sources)}, Exemples: {len(processed_examples)}, Nouveaux: {len(processed_new_sources)}")
                
                # Stockage dans la session avec logs
                logger.debug("Stockage des documents traités dans la session")
                st.session_state.processed_old_sources = processed_old_sources
                st.session_state.processed_examples = processed_examples
                st.session_state.processed_new_sources = processed_new_sources
                
                # Gestion sécurisée de la description utilisateur
                if user_description and user_description.strip():
                    logger.info(f"Description utilisateur fournie: {len(user_description)} caractères")
                    if 'user_description' not in st.session_state:
                        st.session_state.user_description = user_description
                        logger.debug("Description utilisateur stockée pour la première fois")
                    else:
                        # Éviter le conflit de clés en utilisant une clé temporaire
                        st.session_state.temp_user_description = user_description
                        logger.debug("Description utilisateur stockée temporairement pour éviter les conflits")
                else:
                    logger.debug("Aucune description utilisateur fournie")
                
                st.session_state.files_processed = True
                
                # Affichage des résultats
                if processed_old_sources:
                    st.success(f"✅ {len(processed_old_sources)} document(s) source(s) ancien(s) traité(s)")
                if processed_examples:
                    st.success(f"✅ {len(processed_examples)} document(s) exemple(s) traité(s)")
                if processed_new_sources:
                    st.success(f"✅ {len(processed_new_sources)} nouveau(x) document(s) source(s) traité(s)")
                
                st.rerun()
                
            except Exception as e:
                logger.error(f"Erreur lors du traitement des fichiers: {str(e)}", exc_info=True)
                st.error(f"❌ Erreur lors du traitement: {str(e)}")
                # Afficher des détails supplémentaires en mode debug
                if logger.isEnabledFor(logging.DEBUG):
                    st.exception(e)
    
    # Affichage des fichiers traités
    if st.session_state.get('files_processed', False):
        show_processed_files_summary()

def show_processed_files_summary():
    """
    Affiche un résumé des fichiers traités avec l'architecture 3+1.
    """
    st.markdown("---")
    st.subheader("📋 Fichiers traités")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.get('processed_old_sources'):
            st.markdown("**📜 Sources anciennes:**")
            for i, doc in enumerate(st.session_state.processed_old_sources, 1):
                metadata = doc.get('metadata', {})
                filename = metadata.get('original_filename', f'Ancien {i}')
                length = metadata.get('processed_length', 0)
                st.write(f"• {filename} ({length:,} caractères)")
    
    with col2:
        if st.session_state.get('processed_examples'):
            st.markdown("**🎨 Exemples construits:**")
            for i, doc in enumerate(st.session_state.processed_examples, 1):
                metadata = doc.get('metadata', {})
                filename = metadata.get('original_filename', f'Exemple {i}')
                length = metadata.get('processed_length', 0)
                st.write(f"• {filename} ({length:,} caractères)")
    
    with col3:
        if st.session_state.get('processed_new_sources'):
            st.markdown("**📄 Nouvelles sources:**")
            for i, doc in enumerate(st.session_state.processed_new_sources, 1):
                metadata = doc.get('metadata', {})
                filename = metadata.get('original_filename', f'Nouveau {i}')
                length = metadata.get('processed_length', 0)
                st.write(f"• {filename} ({length:,} caractères)")
    
    # Afficher la description utilisateur si présente
    if st.session_state.get('user_description'):
        st.markdown("**💬 Description utilisateur:**")
        st.info(st.session_state.user_description)

def show_generation_section():
    """
    Section de génération du document avec architecture 3+1.
    """
    st.markdown("---")
    st.subheader("🤖 Génération intelligente")
    
    # Information sur la transformation
    st.info("🧠 **Intelligence de transformation** : L'IA va analyser comment le document source ancien a été transformé en exemple construit, puis appliquer cette même transformation sur vos nouveaux documents sources.")
    
    # Afficher la description utilisateur déjà saisie
    current_description = st.session_state.get('user_description') or st.session_state.get('temp_user_description')
    if current_description:
        logger.debug(f"Affichage de la description utilisateur: {len(current_description)} caractères")
        st.markdown("**💬 Votre description :**")
        st.write(f"*{current_description}*")
        
        if st.button("✏️ Modifier la description", key="edit_description"):
            logger.info("Utilisateur souhaite modifier la description")
            st.session_state.edit_description = True
    
    # Permettre la modification de la description
    if st.session_state.get('edit_description', False):
        new_description = st.text_area(
            "Modifier votre description",
            value=st.session_state.get('user_description', ''),
            placeholder="Ex: Créer un rapport technique, adapter le ton pour un public jeune...",
            height=100,
            key="edit_user_description"  # Clé unique pour éviter les conflits
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Sauvegarder", type="primary", key="save_description"):
                logger.info(f"Sauvegarde de la nouvelle description: {len(new_description)} caractères")
                try:
                    # Nettoyer les anciennes valeurs pour éviter les conflits
                    if 'temp_user_description' in st.session_state:
                        del st.session_state.temp_user_description
                        logger.debug("Suppression de temp_user_description")
                    
                    st.session_state.user_description = new_description
                    st.session_state.edit_description = False
                    logger.debug("Description sauvegardée avec succès")
                    st.rerun()
                except Exception as e:
                    logger.error(f"Erreur lors de la sauvegarde de la description: {str(e)}")
                    st.error(f"Erreur lors de la sauvegarde: {str(e)}")
        with col2:
            if st.button("❌ Annuler", key="cancel_description"):
                logger.info("Annulation de la modification de description")
                st.session_state.edit_description = False
                st.rerun()
    
    # Configuration de génération
    with st.expander("🔧 Paramètres de génération"):
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider(
                "Créativité (Temperature)",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="Plus élevé = plus créatif, plus bas = plus conservateur"
            )
            
            max_tokens = st.number_input(
                "Longueur maximale (tokens)",
                min_value=500,
                max_value=4000,
                value=2000,
                step=100,
                help="Nombre maximum de tokens pour la génération"
            )
        
        with col2:
            top_p = st.slider(
                "Diversité (Top-p)",
                min_value=0.1,
                max_value=1.0,
                value=0.9,
                step=0.1,
                help="Contrôle la diversité du vocabulaire"
            )
            
            presence_penalty = st.slider(
                "Éviter les répétitions",
                min_value=0.0,
                max_value=2.0,
                value=0.1,
                step=0.1,
                help="Pénalise la répétition de mots"
            )
    
    # Bouton de génération
    if st.button("🚀 Générer avec transformation intelligente", type="primary"):
        # Vérifier que nous avons les documents nécessaires
        if not st.session_state.get('processed_old_sources') and not st.session_state.get('processed_examples') and not st.session_state.get('processed_new_sources'):
            st.error("Veuillez d'abord traiter vos documents dans la section upload.")
            return
        
        # Configuration de génération
        generation_config = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "presence_penalty": presence_penalty
        }
        
        with st.spinner("🧠 Analyse de la transformation et génération en cours..."):
            try:
                # Récupérer la description utilisateur (priorité à temp_user_description)
                user_desc = st.session_state.get('temp_user_description') or st.session_state.get('user_description')
                
                logger.info("Début de la génération de document")
                logger.debug(f"Documents anciens: {len(st.session_state.get('processed_old_sources', []))}")
                logger.debug(f"Documents exemples: {len(st.session_state.get('processed_examples', []))}")
                logger.debug(f"Nouveaux documents: {len(st.session_state.get('processed_new_sources', []))}")
                logger.debug(f"Description utilisateur: {'Oui' if user_desc else 'Non'}")
                
                # Génération du document avec la nouvelle architecture 3+1
                result = st.session_state.document_service.generate_document(
                    old_source_documents=st.session_state.get('processed_old_sources', []),
                    example_documents=st.session_state.get('processed_examples', []),
                    new_source_documents=st.session_state.get('processed_new_sources', []),
                    user_description=user_desc,
                    generation_config=generation_config
                )
                
                logger.info(f"Génération terminée - Succès: {result.get('success', False)}")
                
                if result['success']:
                    logger.info("Document généré avec succès")
                    st.session_state.generated_document = result['content']
                    st.session_state.generation_metadata = result['metadata']
                    st.session_state.document_generated = True
                    
                    # Nettoyer la description temporaire après génération réussie
                    if 'temp_user_description' in st.session_state:
                        if not st.session_state.get('user_description'):
                            st.session_state.user_description = st.session_state.temp_user_description
                        del st.session_state.temp_user_description
                        logger.debug("Description temporaire nettoyée après génération")
                    
                    st.success("✅ Document généré avec transformation intelligente !")
                    st.rerun()
                else:
                    logger.error(f"Échec de la génération: {result.get('error', 'Erreur inconnue')}")
                    st.error(f"❌ Erreur lors de la génération: {result.get('error', 'Erreur inconnue')}")
                    
            except Exception as e:
                logger.error(f"Exception lors de la génération: {str(e)}", exc_info=True)
                st.error(f"❌ Erreur lors de la génération: {str(e)}")
                # Afficher des détails supplémentaires en mode debug
                if logger.isEnabledFor(logging.DEBUG):
                    st.exception(e)

def show_results_section():
    """
    Section d'affichage et d'export des résultats.
    """
    st.markdown("---")
    st.subheader("📄 Document généré")
    
    if not st.session_state.get('generated_document'):
        return
    
    # Métadonnées de génération
    metadata = st.session_state.get('generation_metadata', {})
    content_stats = metadata.get('content_stats', {})
    
    # Statistiques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Caractères", f"{content_stats.get('character_count', 0):,}")
    with col2:
        st.metric("Mots", f"{content_stats.get('word_count', 0):,}")
    with col3:
        st.metric("Lignes", f"{content_stats.get('line_count', 0):,}")
    with col4:
        generated_at = metadata.get('generated_at', '')
        if generated_at:
            time_str = datetime.fromisoformat(generated_at.replace('Z', '+00:00')).strftime('%H:%M:%S')
            st.metric("Généré à", time_str)
    
    # Affichage du document
    st.markdown("**Prévisualisation:**")
    
    # Onglets pour différents modes d'affichage
    tab1, tab2 = st.tabs(["📖 Rendu Markdown", "📝 Code Markdown"])
    
    with tab1:
        # Affichage du Markdown rendu avec styles améliorés
        try:
            # Wrapper avec classe CSS pour le styling
            markdown_content = f'<div class="markdown-content">{st.session_state.generated_document}</div>'
            st.markdown(markdown_content, unsafe_allow_html=True)
        except Exception as e:
            logger.warning(f"Erreur lors du rendu Markdown avancé: {str(e)}")
            # Fallback vers le rendu standard
            st.markdown(st.session_state.generated_document)
            
        # Séparateur
        st.markdown("---")
        
        # Alternative avec st.write pour une meilleure compatibilité
        st.markdown("**📖 Rendu alternatif (compatibilité étendue):**")
        with st.container():
            st.write(st.session_state.generated_document)
    
    with tab2:
        # Affichage du code Markdown
        st.code(st.session_state.generated_document, language='markdown')
    
    # Section d'export
    st.markdown("---")
    st.subheader("💾 Export du document")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export Markdown
        st.download_button(
            label="📝 Télécharger Markdown",
            data=st.session_state.generated_document,
            file_name=f"document_genere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    with col2:
        # Export PDF
        if st.button("📄 Générer PDF"):
            try:
                with st.spinner("Génération du PDF..."):
                    pdf_converter = MarkdownToPDFConverter()
                    
                    if not pdf_converter.is_available():
                        st.error("❌ Convertisseur PDF non disponible. Installez weasyprint ou pdfkit.")
                    else:
                        # Fichier temporaire
                        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                            pdf_result = pdf_converter.convert(
                                st.session_state.generated_document,
                                tmp_file.name,
                                metadata={'title': 'Document InspireDoc'}
                            )
                            
                            if pdf_result['success']:
                                with open(tmp_file.name, 'rb') as pdf_file:
                                    st.download_button(
                                        label="📥 Télécharger PDF",
                                        data=pdf_file.read(),
                                        file_name=f"document_genere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                        mime="application/pdf"
                                    )
                                st.success("✅ PDF généré avec succès !")
                            else:
                                st.error(f"❌ Erreur PDF: {pdf_result.get('error')}")
                            
                            # Nettoyage
                            try:
                                os.unlink(tmp_file.name)
                            except:
                                pass
                                
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération PDF: {str(e)}")
    
    with col3:
        # Export DOCX
        if st.button("📄 Générer DOCX"):
            try:
                with st.spinner("Génération du DOCX..."):
                    docx_converter = MarkdownToDOCXConverter()
                    
                    # Fichier temporaire
                    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
                        docx_result = docx_converter.convert(
                            st.session_state.generated_document,
                            tmp_file.name,
                            metadata={'title': 'Document InspireDoc'}
                        )
                        
                        if docx_result['success']:
                            with open(tmp_file.name, 'rb') as docx_file:
                                st.download_button(
                                    label="📥 Télécharger DOCX",
                                    data=docx_file.read(),
                                    file_name=f"document_genere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                            st.success("✅ DOCX généré avec succès !")
                        else:
                            st.error(f"❌ Erreur DOCX: {docx_result.get('error')}")
                        
                        # Nettoyage
                        try:
                            os.unlink(tmp_file.name)
                        except:
                            pass
                            
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération DOCX: {str(e)}")
    
    # Bouton pour recommencer
    st.markdown("---")
    if st.button("🔄 Nouvelle génération"):
        # Réinitialiser la session
        keys_to_reset = ['files_processed', 'document_generated', 'generated_document', 
                        'generation_metadata', 'processed_sources', 'processed_examples']
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()