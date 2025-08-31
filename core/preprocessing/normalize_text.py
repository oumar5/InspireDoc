import re
import unicodedata
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class TextNormalizer:
    """
    Classe pour normaliser le texte (casse, accents, ponctuation, etc.).
    """
    
    def __init__(self,
                 lowercase: bool = False,
                 remove_accents: bool = False,
                 normalize_punctuation: bool = True,
                 normalize_quotes: bool = True,
                 normalize_dashes: bool = True,
                 normalize_spaces: bool = True,
                 fix_encoding: bool = True):
        """
        Initialise le normalisateur de texte.
        
        Args:
            lowercase: Convertir en minuscules
            remove_accents: Supprimer les accents
            normalize_punctuation: Normaliser la ponctuation
            normalize_quotes: Normaliser les guillemets
            normalize_dashes: Normaliser les tirets
            normalize_spaces: Normaliser les espaces
            fix_encoding: Corriger les problèmes d'encodage
        """
        self.lowercase = lowercase
        self.remove_accents = remove_accents
        self.normalize_punctuation = normalize_punctuation
        self.normalize_quotes = normalize_quotes
        self.normalize_dashes = normalize_dashes
        self.normalize_spaces = normalize_spaces
        self.fix_encoding = fix_encoding
        
        self._init_patterns()
    
    def _init_patterns(self):
        """
        Initialise les patterns de normalisation.
        """
        # Guillemets et apostrophes
        self.quotes_pattern = re.compile(r'[`´]')
        self.double_quotes_pattern = re.compile(r'[«»]')
        
        # Tirets et traits d'union
        self.dashes_pattern = re.compile(r'[–—―]')
        
        # Espaces spéciaux
        self.special_spaces_pattern = re.compile(r'[\u00A0\u2000-\u200B\u2028\u2029\u202F\u205F\u3000]')
        
        # Points de suspension
        self.ellipsis_pattern = re.compile(r'…')
        
        # Problèmes d'encodage courants
        self.encoding_fixes = {
            'Ã©': 'é', 'Ã¨': 'è', 'Ã ': 'à', 'Ã§': 'ç', 'Ã´': 'ô', 'Ã¢': 'â', 
            'Ãª': 'ê', 'Ã®': 'î', 'Ã¹': 'ù', 'Ã»': 'û', 'Ã¯': 'ï', 'Ã«': 'ë',
            'Â': ''
        }
    
    def normalize(self, text: str) -> Dict[str, Any]:
        """
        Normalise le texte selon les paramètres configurés.
        
        Args:
            text: Texte à normaliser
            
        Returns:
            Dictionnaire avec le texte normalisé et les statistiques
        """
        if not text:
            return {
                "normalized_text": "",
                "normalization_stats": {
                    "original_length": 0,
                    "normalized_length": 0,
                    "normalization_steps": []
                }
            }
        
        original_length = len(text)
        normalized_text = text
        normalization_steps = []
        
        # Étape 1: Corriger les problèmes d'encodage
        if self.fix_encoding:
            before_length = len(normalized_text)
            normalized_text = self._fix_encoding_issues(normalized_text)
            if len(normalized_text) != before_length:
                normalization_steps.append("Problèmes d'encodage corrigés")
        
        # Étape 2: Normalisation Unicode
        before_length = len(normalized_text)
        normalized_text = unicodedata.normalize('NFKC', normalized_text)
        if len(normalized_text) != before_length:
            normalization_steps.append("Normalisation Unicode appliquée")
        
        # Étape 3: Normaliser les espaces spéciaux
        if self.normalize_spaces:
            before_text = normalized_text
            normalized_text = self.special_spaces_pattern.sub(' ', normalized_text)
            if normalized_text != before_text:
                normalization_steps.append("Espaces spéciaux normalisés")
        
        # Étape 4: Normaliser les guillemets
        if self.normalize_quotes:
            before_text = normalized_text
            normalized_text = self.quotes_pattern.sub("'", normalized_text)
            normalized_text = self.double_quotes_pattern.sub('"', normalized_text)
            if normalized_text != before_text:
                normalization_steps.append("Guillemets normalisés")
        
        # Étape 5: Normaliser les tirets
        if self.normalize_dashes:
            before_text = normalized_text
            normalized_text = self.dashes_pattern.sub('-', normalized_text)
            if normalized_text != before_text:
                normalization_steps.append("Tirets normalisés")
        
        # Étape 6: Normaliser la ponctuation
        if self.normalize_punctuation:
            before_text = normalized_text
            # Points de suspension
            normalized_text = self.ellipsis_pattern.sub('...', normalized_text)
            # Espaces avant la ponctuation
            normalized_text = re.sub(r'\s+([.!?:;,])', r'\1', normalized_text)
            # Espaces après la ponctuation
            normalized_text = re.sub(r'([.!?:;,])([A-Za-z])', r'\1 \2', normalized_text)
            if normalized_text != before_text:
                normalization_steps.append("Ponctuation normalisée")
        
        # Étape 7: Supprimer les accents si demandé
        if self.remove_accents:
            before_text = normalized_text
            normalized_text = self._remove_accents(normalized_text)
            if normalized_text != before_text:
                normalization_steps.append("Accents supprimés")
        
        # Étape 8: Convertir en minuscules si demandé
        if self.lowercase:
            before_text = normalized_text
            normalized_text = normalized_text.lower()
            if normalized_text != before_text:
                normalization_steps.append("Converti en minuscules")
        
        # Nettoyage final des espaces
        normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()
        
        # Statistiques
        normalization_stats = {
            "original_length": original_length,
            "normalized_length": len(normalized_text),
            "length_change": len(normalized_text) - original_length,
            "normalization_steps": normalization_steps
        }
        
        logger.info(f"Texte normalisé: {original_length} -> {len(normalized_text)} caractères")
        
        return {
            "normalized_text": normalized_text,
            "normalization_stats": normalization_stats
        }
    
    def _fix_encoding_issues(self, text: str) -> str:
        """
        Corrige les problèmes d'encodage courants.
        
        Args:
            text: Texte avec des problèmes d'encodage potentiels
            
        Returns:
            Texte avec encodage corrigé
        """
        fixed_text = text
        
        for wrong, correct in self.encoding_fixes.items():
            fixed_text = fixed_text.replace(wrong, correct)
        
        return fixed_text
    
    def _remove_accents(self, text: str) -> str:
        """
        Supprime les accents du texte.
        
        Args:
            text: Texte avec accents
            
        Returns:
            Texte sans accents
        """
        # Décomposer les caractères Unicode
        nfkd_form = unicodedata.normalize('NFD', text)
        
        # Supprimer les marques diacritiques
        without_accents = ''.join([
            char for char in nfkd_form 
            if unicodedata.category(char) != 'Mn'
        ])
        
        return without_accents
    
    def normalize_for_search(self, text: str) -> str:
        """
        Normalisation spécialisée pour la recherche.
        
        Args:
            text: Texte à normaliser
            
        Returns:
            Texte normalisé pour la recherche
        """
        # Configuration spéciale pour la recherche
        original_config = {
            'lowercase': self.lowercase,
            'remove_accents': self.remove_accents,
            'normalize_punctuation': self.normalize_punctuation,
            'normalize_quotes': self.normalize_quotes,
            'normalize_dashes': self.normalize_dashes,
            'normalize_spaces': self.normalize_spaces,
            'fix_encoding': self.fix_encoding
        }
        
        # Configuration optimisée pour la recherche
        self.lowercase = True
        self.remove_accents = True
        self.normalize_punctuation = True
        self.normalize_quotes = True
        self.normalize_dashes = True
        self.normalize_spaces = True
        self.fix_encoding = True
        
        result = self.normalize(text)
        normalized_text = result['normalized_text']
        
        # Restaurer la configuration originale
        for key, value in original_config.items():
            setattr(self, key, value)
        
        return normalized_text
    
    def normalize_for_llm(self, text: str) -> str:
        """
        Normalisation spécialisée pour les LLMs.
        
        Args:
            text: Texte à normaliser
            
        Returns:
            Texte normalisé pour LLM
        """
        # Configuration spéciale pour LLM (préserver la casse et les accents)
        original_config = {
            'lowercase': self.lowercase,
            'remove_accents': self.remove_accents,
            'normalize_punctuation': self.normalize_punctuation,
            'normalize_quotes': self.normalize_quotes,
            'normalize_dashes': self.normalize_dashes,
            'normalize_spaces': self.normalize_spaces,
            'fix_encoding': self.fix_encoding
        }
        
        # Configuration optimisée pour LLM
        self.lowercase = False  # Préserver la casse
        self.remove_accents = False  # Préserver les accents
        self.normalize_punctuation = True
        self.normalize_quotes = True
        self.normalize_dashes = True
        self.normalize_spaces = True
        self.fix_encoding = True
        
        result = self.normalize(text)
        normalized_text = result['normalized_text']
        
        # Restaurer la configuration originale
        for key, value in original_config.items():
            setattr(self, key, value)
        
        return normalized_text