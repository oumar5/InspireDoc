import os
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Imports des modules InspireDoc
from core.ingestion.load_pdf import PDFLoader
from core.ingestion.load_txt import TXTLoader
from core.ingestion.load_docx import DOCXLoader
from core.preprocessing.clean_text import TextCleaner
from core.preprocessing.normalize_text import TextNormalizer
from core.llm.prompt_builder import PromptBuilder
from core.llm.call_model import LLMCaller
from core.utils.helpers import (
    generate_unique_filename, 
    validate_file_extension, 
    ensure_directory_exists,
    format_file_size
)
from config.settings import Settings

logger = logging.getLogger(__name__)

class DocumentService:
    """
    Service principal pour orchestrer la génération de documents InspireDoc.
    """
    
    def __init__(self):
        """
        Initialise le service de documents.
        """
        # Validation de la configuration
        if not Settings.validate_config():
            raise ValueError("Configuration InspireDoc invalide. Vérifiez les variables d'environnement.")
        
        # Initialisation des composants
        self.pdf_loader = PDFLoader()
        self.txt_loader = TXTLoader()
        self.docx_loader = DOCXLoader()
        
        self.text_cleaner = TextCleaner()
        self.text_normalizer = TextNormalizer()
        
        self.prompt_builder = PromptBuilder()
        self.llm_caller = LLMCaller()
        
        # Assurer que les dossiers existent
        ensure_directory_exists(Settings.get_upload_path())
        ensure_directory_exists(Settings.get_processed_path())
        ensure_directory_exists(Settings.get_exports_path())
        
        logger.info("✅ DocumentService initialisé avec succès")
    
    def process_uploaded_files(self, 
                              old_source_files: List[Any],
                              example_files: List[Any],
                              new_source_files: List[Any],
                              old_source_text: str = "",
                              example_text: str = "",
                              new_source_text: str = "") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Traite les fichiers uploadés et/ou le texte saisi (3 types de documents).
        
        Args:
            old_source_files: Liste des documents sources anciens
            example_files: Liste des documents exemples construits
            new_source_files: Liste des nouveaux documents sources
            old_source_text: Texte saisi pour document source ancien
            example_text: Texte saisi pour document exemple
            new_source_text: Texte saisi pour nouveau document source
            
        Returns:
            Tuple (old_sources, examples, new_sources)
        """
        try:
            processed_old_sources = []
            processed_examples = []
            processed_new_sources = []
            
            # Traitement des anciens documents sources
            for file in old_source_files:
                if file is not None:
                    result = self._process_single_file(file, "old_source")
                    if result:
                        processed_old_sources.append(result)
            
            # Traitement des documents exemples
            for file in example_files:
                if file is not None:
                    result = self._process_single_file(file, "example")
                    if result:
                        processed_examples.append(result)
            
            # Traitement des nouveaux documents sources
            for file in new_source_files:
                if file is not None:
                    result = self._process_single_file(file, "new_source")
                    if result:
                        processed_new_sources.append(result)
            
            # Traitement du texte saisi directement
            if old_source_text.strip():
                text_doc = self._create_text_document(old_source_text, "Document source ancien (texte)", "old_source")
                processed_old_sources.append(text_doc)
            
            if example_text.strip():
                text_doc = self._create_text_document(example_text, "Document exemple (texte)", "example")
                processed_examples.append(text_doc)
            
            if new_source_text.strip():
                text_doc = self._create_text_document(new_source_text, "Nouveau document source (texte)", "new_source")
                processed_new_sources.append(text_doc)
            
            logger.info(f"Documents traités: {len(processed_old_sources)} anciens, {len(processed_examples)} exemples, {len(processed_new_sources)} nouveaux")
            
            return processed_old_sources, processed_examples, processed_new_sources
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement des fichiers: {str(e)}")
            raise
    
    def _process_single_file(self, file, file_type: str) -> Optional[Dict[str, Any]]:
        """
        Traite un seul fichier uploadé.
        
        Args:
            file: Fichier uploadé (Streamlit UploadedFile)
            file_type: Type de fichier ("source" ou "example")
            
        Returns:
            Dictionnaire avec le contenu traité ou None si erreur
        """
        try:
            # Validation du fichier
            if not validate_file_extension(file.name, Settings.SUPPORTED_FORMATS):
                logger.warning(f"Format de fichier non supporté: {file.name}")
                return None
            
            # Vérification de la taille
            file_size = len(file.getvalue())
            if file_size > Settings.MAX_FILE_SIZE_MB * 1024 * 1024:
                logger.warning(f"Fichier trop volumineux: {file.name} ({format_file_size(file_size)})")
                return None
            
            # Sauvegarde temporaire
            unique_filename = generate_unique_filename(file.name)
            temp_path = os.path.join(Settings.get_upload_path(), unique_filename)
            
            with open(temp_path, "wb") as f:
                f.write(file.getvalue())
            
            # Extraction du contenu
            extracted_data = self._extract_content(temp_path, file.name)
            
            if not extracted_data or not extracted_data.get('text'):
                logger.warning(f"Impossible d'extraire le contenu de {file.name}")
                return None
            
            # Nettoyage et normalisation
            cleaned_result = self.text_cleaner.clean_for_llm(extracted_data['text'])
            normalized_text = self.text_normalizer.normalize_for_llm(cleaned_result)
            
            # Métadonnées du fichier traité
            processed_metadata = {
                **extracted_data.get('metadata', {}),
                'original_filename': file.name,
                'unique_filename': unique_filename,
                'file_type': file_type,
                'file_size': file_size,
                'processed_at': datetime.now().isoformat(),
                'original_length': len(extracted_data['text']),
                'processed_length': len(normalized_text)
            }
            
            # Nettoyage du fichier temporaire
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"Impossible de supprimer le fichier temporaire {temp_path}: {str(e)}")
            
            logger.info(f"Fichier traité avec succès: {file.name} -> {len(normalized_text)} caractères")
            
            return {
                'text': normalized_text,
                'metadata': processed_metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du fichier {file.name}: {str(e)}")
            return None
    
    def _create_text_document(self, text_content: str, title: str, doc_type: str) -> Dict[str, Any]:
        """
        Crée un document à partir de texte saisi directement.
        
        Args:
            text_content: Contenu textuel
            title: Titre du document
            doc_type: Type de document (old_source, example, new_source)
            
        Returns:
            Dictionnaire représentant le document
        """
        try:
            # Nettoyage et normalisation du texte
            cleaned_text = self.text_cleaner.clean_text(text_content)
            normalized_text = self.text_normalizer.normalize_text(cleaned_text)
            
            return {
                'title': title,
                'content': normalized_text,
                'original_content': text_content,
                'file_type': 'text',
                'file_size': len(text_content.encode('utf-8')),
                'processed_at': datetime.now().isoformat(),
                'document_type': doc_type,
                'source': 'text_input',
                'metadata': {
                    'character_count': len(text_content),
                    'word_count': len(text_content.split()),
                    'line_count': len(text_content.splitlines())
                }
            }
        except Exception as e:
            logger.error(f"Erreur lors de la création du document texte: {str(e)}")
            return {
                'title': title,
                'content': text_content,
                'original_content': text_content,
                'file_type': 'text',
                'file_size': len(text_content.encode('utf-8')),
                'processed_at': datetime.now().isoformat(),
                'document_type': doc_type,
                'source': 'text_input',
                'error': str(e)
            }
            
            # Nettoyage du fichier temporaire
            try:
                os.remove(temp_path)
            except Exception as e:
                logger.warning(f"Impossible de supprimer le fichier temporaire {temp_path}: {str(e)}")
            
            logger.info(f"Fichier traité avec succès: {file.name} -> {len(normalized_text)} caractères")
            
            return {
                'text': normalized_text,
                'metadata': processed_metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement du fichier {file.name}: {str(e)}")
            return None
    
    def _extract_content(self, file_path: str, original_name: str) -> Optional[Dict[str, Any]]:
        """
        Extrait le contenu d'un fichier selon son type.
        
        Args:
            file_path: Chemin vers le fichier
            original_name: Nom original du fichier
            
        Returns:
            Dictionnaire avec le texte extrait et les métadonnées
        """
        try:
            file_ext = Path(original_name).suffix.lower().lstrip('.')
            
            if file_ext == 'pdf':
                return self.pdf_loader.load(file_path)
            elif file_ext == 'txt':
                return self.txt_loader.load(file_path)
            elif file_ext == 'docx':
                return self.docx_loader.load(file_path)
            else:
                logger.error(f"Type de fichier non supporté: {file_ext}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction du contenu de {file_path}: {str(e)}")
            return None
    
    def generate_document(self, 
                         old_source_documents: List[Dict[str, Any]],
                         example_documents: List[Dict[str, Any]],
                         new_source_documents: List[Dict[str, Any]],
                         user_description: Optional[str] = None,
                         generation_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Génère un nouveau document basé sur l'architecture 3+1.
        
        Args:
            old_source_documents: Documents sources anciens (référence)
            example_documents: Documents exemples construits (transformation)
            new_source_documents: Nouveaux documents sources (à traiter)
            user_description: Description optionnelle de l'utilisateur
            generation_config: Configuration pour la génération
            
        Returns:
            Dictionnaire avec le document généré et les métadonnées
        """
        try:
            # Validation des entrées
            if not old_source_documents and not example_documents and not new_source_documents:
                raise ValueError("Au moins un document de chaque type est recommandé")
            
            # Construction du prompt avec la nouvelle logique 3+1
            logger.info("Construction du prompt de génération avec architecture 3+1...")
            prompt_data = self.prompt_builder.build_transformation_prompt(
                old_source_documents=old_source_documents,
                example_documents=example_documents,
                new_source_documents=new_source_documents,
                user_description=user_description
            )
            
            # Validation du prompt
            if not self.prompt_builder.validate_prompt(prompt_data):
                raise ValueError("Prompt généré invalide")
            
            # Génération via LLM
            logger.info("Génération du document via LLM...")
            generation_result = self.llm_caller.generate_document(
                prompt_data=prompt_data,
                generation_config=generation_config
            )
            
            if not generation_result["success"]:
                error_msg = generation_result.get("error", "Erreur inconnue lors de la génération")
                raise RuntimeError(f"Échec de la génération: {error_msg}")
            
            # Métadonnées de la génération
            generation_metadata = {
                'generated_at': datetime.now().isoformat(),
                'old_source_count': len(old_source_documents),
                'example_count': len(example_documents),
                'new_source_count': len(new_source_documents),
                'user_description': user_description,
                'prompt_metadata': prompt_data['metadata'],
                'llm_metadata': generation_result['metadata'],
                'content_stats': {
                    'character_count': len(generation_result['content']),
                    'word_count': len(generation_result['content'].split()),
                    'line_count': len(generation_result['content'].splitlines())
                }
            }
            
            logger.info(f"Document généré avec succès: {generation_metadata['content_stats']['character_count']} caractères")
            
            return {
                'success': True,
                'content': generation_result['content'],
                'metadata': generation_metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du document: {str(e)}")
            return {
                'success': False,
                'content': '',
                'error': str(e),
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'error': str(e)
                }
            }
    
    def save_generated_document(self, content: str, filename: str = None) -> str:
        """
        Sauvegarde un document généré.
        
        Args:
            content: Contenu du document
            filename: Nom de fichier optionnel
            
        Returns:
            Chemin vers le fichier sauvegardé
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"document_genere_{timestamp}.md"
            
            # Assurer l'extension .md
            if not filename.endswith('.md'):
                filename += '.md'
            
            file_path = os.path.join(Settings.get_exports_path(), filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Document sauvegardé: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {str(e)}")
            raise
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Retourne le statut du service.
        
        Returns:
            Dictionnaire avec le statut des composants
        """
        try:
            llm_status = self.llm_caller.test_connection()
            
            return {
                'service_initialized': True,
                'llm_connection': llm_status,
                'directories_ready': {
                    'uploads': os.path.exists(Settings.get_upload_path()),
                    'processed': os.path.exists(Settings.get_processed_path()),
                    'exports': os.path.exists(Settings.get_exports_path())
                },
                'supported_formats': Settings.SUPPORTED_FORMATS,
                'max_file_size_mb': Settings.MAX_FILE_SIZE_MB,
                'llm_info': self.llm_caller.get_model_info()
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification du statut: {str(e)}")
            return {
                'service_initialized': False,
                'error': str(e)
            }