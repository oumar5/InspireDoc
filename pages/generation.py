import streamlit as st
import os
import tempfile
from typing import List, Dict, Any, Optional
from datetime import datetime

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
        **Documents sources** : Contiennent les informations que vous voulez utiliser dans le nouveau document.
        
        **Documents exemples** : Servent de modèle pour le style, la structure et la mise en forme.
        
        **Formats supportés** : PDF, TXT, DOCX (max 10 MB par fichier)
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 Documents sources (contenu)**")
        source_files = st.file_uploader(
            "Choisissez vos documents sources",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            key="source_files",
            help="Ces documents fourniront le contenu pour votre nouveau document"
        )
    
    with col2:
        st.markdown("**🎨 Documents exemples (style)**")
        example_files = st.file_uploader(
            "Choisissez vos documents exemples",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            key="example_files",
            help="Ces documents serviront de modèle pour le style et la structure"
        )
    
    # Bouton de traitement
    if st.button("🔄 Traiter les fichiers", type="primary"):
        if not source_files and not example_files:
            st.error("Veuillez uploader au moins un document source ou exemple.")
            return
        
        with st.spinner("Traitement des fichiers en cours..."):
            try:
                # Traitement des fichiers
                processed_sources, processed_examples = st.session_state.document_service.process_uploaded_files(
                    source_files or [],
                    example_files or []
                )
                
                # Stockage dans la session
                st.session_state.processed_sources = processed_sources
                st.session_state.processed_examples = processed_examples
                st.session_state.files_processed = True
                
                # Affichage des résultats
                if processed_sources:
                    st.success(f"✅ {len(processed_sources)} document(s) source(s) traité(s)")
                if processed_examples:
                    st.success(f"✅ {len(processed_examples)} document(s) exemple(s) traité(s)")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erreur lors du traitement: {str(e)}")
    
    # Affichage des fichiers traités
    if st.session_state.get('files_processed', False):
        show_processed_files_summary()

def show_processed_files_summary():
    """
    Affiche un résumé des fichiers traités.
    """
    st.markdown("---")
    st.subheader("📋 Fichiers traités")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.get('processed_sources'):
            st.markdown("**Sources:**")
            for i, doc in enumerate(st.session_state.processed_sources, 1):
                metadata = doc.get('metadata', {})
                filename = metadata.get('original_filename', f'Source {i}')
                length = metadata.get('processed_length', 0)
                st.write(f"• {filename} ({length:,} caractères)")
    
    with col2:
        if st.session_state.get('processed_examples'):
            st.markdown("**Exemples:**")
            for i, doc in enumerate(st.session_state.processed_examples, 1):
                metadata = doc.get('metadata', {})
                filename = metadata.get('original_filename', f'Exemple {i}')
                length = metadata.get('processed_length', 0)
                st.write(f"• {filename} ({length:,} caractères)")

def show_generation_section():
    """
    Section de génération du document.
    """
    st.markdown("---")
    st.subheader("🤖 Génération du document")
    
    # Demande de génération
    generation_request = st.text_area(
        "Décrivez le document que vous souhaitez générer",
        placeholder="Ex: Rédigez un rapport technique sur les résultats de l'étude, en suivant le format du document exemple...",
        height=100,
        help="Soyez précis sur le type de document, le ton, et les éléments importants à inclure"
    )
    
    # Instructions supplémentaires (optionnel)
    with st.expander("⚙️ Instructions supplémentaires (optionnel)"):
        additional_instructions = st.text_area(
            "Instructions spécifiques",
            placeholder="Ex: Utilisez un ton formel, incluez des sous-titres, limitez à 2 pages...",
            height=80
        )
    
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
    if st.button("🚀 Générer le document", type="primary"):
        if not generation_request.strip():
            st.error("Veuillez décrire le document que vous souhaitez générer.")
            return
        
        # Configuration de génération
        generation_config = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "presence_penalty": presence_penalty
        }
        
        with st.spinner("Génération en cours... Cela peut prendre quelques instants."):
            try:
                # Génération du document
                result = st.session_state.document_service.generate_document(
                    source_documents=st.session_state.get('processed_sources', []),
                    example_documents=st.session_state.get('processed_examples', []),
                    generation_request=generation_request,
                    additional_instructions=additional_instructions if 'additional_instructions' in locals() else None,
                    generation_config=generation_config
                )
                
                if result['success']:
                    st.session_state.generated_document = result['content']
                    st.session_state.generation_metadata = result['metadata']
                    st.session_state.document_generated = True
                    
                    st.success("✅ Document généré avec succès !")
                    st.rerun()
                else:
                    st.error(f"❌ Erreur lors de la génération: {result.get('error', 'Erreur inconnue')}")
                    
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération: {str(e)}")

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
        # Affichage du Markdown rendu
        st.markdown(st.session_state.generated_document)
    
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