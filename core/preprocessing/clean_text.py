import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class TextCleaner:
    """
    Classe pour nettoyer et préprocesser le texte extrait des documents.
    """
    
    def __init__(self, 
                 remove_extra_whitespace: bool = True,
                 remove_special_chars: bool = True,
                 remove_page_breaks: bool = True,
                 remove_metadata: bool = True,
                 preserve_structure: bool = True):
        """
        Initialise le nettoyeur de texte.
        
        Args:
            remove_extra_whitespace: Supprimer les espaces multiples
            remove_special_chars: Supprimer les caractères spéciaux inutiles
            remove_page_breaks: Supprimer les sauts de page
            remove_metadata: Supprimer les métadonnées apparentes
            preserve_structure: Préserver la structure (titres, listes, etc.)
        """
        self.remove_extra_whitespace = remove_extra_whitespace
        self.remove_special_chars = remove_special_chars
        self.remove_page_breaks = remove_page_breaks
        self.remove_metadata = remove_metadata
        self.preserve_structure = preserve_structure
        
        # Patterns de nettoyage
        self._init_patterns()
    
    def _init_patterns(self):
        """
        Initialise les patterns regex pour le nettoyage.
        """
        # Sauts de page et caractères de contrôle
        self.page_break_pattern = re.compile(r'\f|\x0c')
        
        # Espaces multiples (mais préserver les sauts de ligne)
        self.multiple_spaces_pattern = re.compile(r'[ \t]+')
        
        # Lignes vides multiples
        self.multiple_newlines_pattern = re.compile(r'\n\s*\n\s*\n+')
        
        # Caractères spéciaux inutiles (mais préserver la ponctuation normale)
        self.special_chars_pattern = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]')
        
        # Métadonnées communes dans les PDFs
        self.metadata_patterns = [
            re.compile(r'Page \d+ of \d+', re.IGNORECASE),
            re.compile(r'\d+/\d+', re.IGNORECASE),
            re.compile(r'Printed on .*', re.IGNORECASE),
            re.compile(r'Generated on .*', re.IGNORECASE),
            re.compile(r'Copyright ©.*', re.IGNORECASE),
            re.compile(r'\[Page \d+\]', re.IGNORECASE)
        ]
        
        # Patterns pour préserver la structure
        self.title_pattern = re.compile(r'^([A-Z][A-Z\s]{2,})$', re.MULTILINE)
        self.bullet_pattern = re.compile(r'^\s*[•·▪▫◦‣⁃]\s+', re.MULTILINE)
        self.number_list_pattern = re.compile(r'^\s*\d+[.):]\s+', re.MULTILINE)
        self.header_pattern = re.compile(r'^#+\s+', re.MULTILINE)
    
    def clean(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Nettoie le texte selon les paramètres configurés.
        
        Args:
            text: Texte à nettoyer
            metadata: Métadonnées optionnelles du document
            
        Returns:
            Dictionnaire avec le texte nettoyé et les statistiques
        """
        if not text:
            return {
                "cleaned_text": "",
                "cleaning_stats": {
                    "original_length": 0,
                    "cleaned_length": 0,
                    "removed_characters": 0,
                    "cleaning_steps": []
                }
            }
        
        original_length = len(text)
        cleaned_text = text
        cleaning_steps = []
        
        # Étape 1: Supprimer les sauts de page
        if self.remove_page_breaks:
            before_length = len(cleaned_text)
            cleaned_text = self.page_break_pattern.sub('\n', cleaned_text)
            removed = before_length - len(cleaned_text)
            if removed > 0:
                cleaning_steps.append(f"Sauts de page supprimés: {removed} caractères")
        
        # Étape 2: Supprimer les caractères de contrôle
        if self.remove_special_chars:
            before_length = len(cleaned_text)
            cleaned_text = self.special_chars_pattern.sub('', cleaned_text)
            removed = before_length - len(cleaned_text)
            if removed > 0:
                cleaning_steps.append(f"Caractères spéciaux supprimés: {removed} caractères")
        
        # Étape 3: Supprimer les métadonnées
        if self.remove_metadata:
            before_length = len(cleaned_text)
            for pattern in self.metadata_patterns:
                cleaned_text = pattern.sub('', cleaned_text)
            removed = before_length - len(cleaned_text)
            if removed > 0:
                cleaning_steps.append(f"Métadonnées supprimées: {removed} caractères")
        
        # Étape 4: Normaliser les espaces
        if self.remove_extra_whitespace:
            before_length = len(cleaned_text)
            # Remplacer les espaces multiples par un seul espace
            cleaned_text = self.multiple_spaces_pattern.sub(' ', cleaned_text)
            # Supprimer les lignes vides multiples
            cleaned_text = self.multiple_newlines_pattern.sub('\n\n', cleaned_text)
            removed = before_length - len(cleaned_text)
            if removed > 0:
                cleaning_steps.append(f"Espaces normalisés: {removed} caractères")
        
        # Étape 5: Nettoyer les débuts et fins de lignes
        lines = cleaned_text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Supprimer les espaces en début et fin de ligne
            line = line.strip()
            
            # Ignorer les lignes très courtes qui sont probablement des artefacts
            if len(line) < 2 and not line.isalnum():
                continue
                
            cleaned_lines.append(line)
        
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Étape 6: Préserver la structure si demandé
        if self.preserve_structure:
            cleaned_text = self._preserve_structure(cleaned_text)
            cleaning_steps.append("Structure préservée")
        
        # Nettoyage final
        cleaned_text = cleaned_text.strip()
        
        # Statistiques
        cleaning_stats = {
            "original_length": original_length,
            "cleaned_length": len(cleaned_text),
            "removed_characters": original_length - len(cleaned_text),
            "cleaning_steps": cleaning_steps,
            "reduction_percentage": round((original_length - len(cleaned_text)) / original_length * 100, 2) if original_length > 0 else 0
        }
        
        logger.info(f"Texte nettoyé: {original_length} -> {len(cleaned_text)} caractères ({cleaning_stats['reduction_percentage']}% de réduction)")
        
        return {
            "cleaned_text": cleaned_text,
            "cleaning_stats": cleaning_stats
        }
    
    def _preserve_structure(self, text: str) -> str:
        """
        Préserve et améliore la structure du texte.
        
        Args:
            text: Texte à structurer
            
        Returns:
            Texte avec structure préservée
        """
        lines = text.split('\n')
        structured_lines = []
        
        for i, line in enumerate(lines):
            if not line.strip():
                structured_lines.append(line)
                continue
            
            # Détecter les titres (lignes en majuscules)
            if self.title_pattern.match(line) and len(line) > 5:
                # Ajouter une ligne vide avant le titre si nécessaire
                if i > 0 and structured_lines and structured_lines[-1].strip():
                    structured_lines.append('')
                structured_lines.append(line)
                # Ajouter une ligne vide après le titre
                structured_lines.append('')
                continue
            
            # Détecter les listes à puces
            if self.bullet_pattern.match(line) or self.number_list_pattern.match(line):
                structured_lines.append(line)
                continue
            
            # Ligne normale
            structured_lines.append(line)
        
        return '\n'.join(structured_lines)
    
    def clean_for_llm(self, text: str) -> str:
        """
        Nettoyage spécialisé pour optimiser le texte pour les LLMs.
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte optimisé pour LLM
        """
        # Configuration spéciale pour LLM
        original_config = {
            'remove_extra_whitespace': self.remove_extra_whitespace,
            'remove_special_chars': self.remove_special_chars,
            'remove_page_breaks': self.remove_page_breaks,
            'remove_metadata': self.remove_metadata,
            'preserve_structure': self.preserve_structure
        }
        
        # Configuration optimisée pour LLM
        self.remove_extra_whitespace = True
        self.remove_special_chars = True
        self.remove_page_breaks = True
        self.remove_metadata = True
        self.preserve_structure = True
        
        result = self.clean(text)
        cleaned_text = result['cleaned_text']
        
        # Optimisations supplémentaires pour LLM
        # Limiter les lignes vides consécutives
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        # S'assurer que les phrases se terminent correctement
        cleaned_text = re.sub(r'([.!?])([A-Z])', r'\1 \2', cleaned_text)
        
        # Restaurer la configuration originale
        for key, value in original_config.items():
            setattr(self, key, value)
        
        return cleaned_text