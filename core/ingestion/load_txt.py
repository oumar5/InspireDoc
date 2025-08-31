import logging
import chardet
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class TXTLoader:
    """
    Classe pour charger et extraire le texte des fichiers TXT.
    """
    
    def __init__(self, default_encoding: str = 'utf-8'):
        """
        Initialise le loader TXT.
        
        Args:
            default_encoding: Encodage par défaut à utiliser
        """
        self.default_encoding = default_encoding
        
    def load(self, file_path: str) -> Dict[str, Any]:
        """
        Charge un fichier TXT et extrait son contenu.
        
        Args:
            file_path: Chemin vers le fichier TXT
            
        Returns:
            Dictionnaire contenant le texte extrait et les métadonnées
        """
        try:
            # Détection automatique de l'encodage
            encoding = self._detect_encoding(file_path)
            
            # Lecture du fichier
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            
            # Métadonnées
            file_stats = Path(file_path).stat()
            metadata = {
                "file_path": file_path,
                "encoding": encoding,
                "file_size_bytes": file_stats.st_size,
                "total_characters": len(content),
                "total_lines": len(content.splitlines()),
                "loader": "txt"
            }
            
            logger.info(f"TXT chargé: {metadata['total_lines']} lignes, {metadata['total_characters']} caractères")
            
            return {
                "text": content,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du TXT {file_path}: {str(e)}")
            return {
                "text": "",
                "metadata": {
                    "error": str(e),
                    "file_path": file_path,
                    "total_characters": 0,
                    "total_lines": 0
                }
            }
    
    def _detect_encoding(self, file_path: str) -> str:
        """
        Détecte l'encodage d'un fichier texte.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            Encodage détecté ou encodage par défaut
        """
        try:
            # Lire un échantillon du fichier pour détecter l'encodage
            with open(file_path, 'rb') as file:
                raw_data = file.read(10000)  # Lire les premiers 10KB
            
            # Utiliser chardet pour détecter l'encodage
            result = chardet.detect(raw_data)
            detected_encoding = result.get('encoding')
            confidence = result.get('confidence', 0)
            
            logger.debug(f"Encodage détecté: {detected_encoding} (confiance: {confidence:.2f})")
            
            # Si la confiance est faible, utiliser l'encodage par défaut
            if confidence < 0.7 or not detected_encoding:
                logger.warning(f"Confiance faible pour l'encodage détecté, utilisation de {self.default_encoding}")
                return self.default_encoding
            
            return detected_encoding
            
        except Exception as e:
            logger.warning(f"Erreur lors de la détection d'encodage: {str(e)}, utilisation de {self.default_encoding}")
            return self.default_encoding
    
    def load_with_encoding(self, file_path: str, encoding: str) -> Dict[str, Any]:
        """
        Charge un fichier TXT avec un encodage spécifique.
        
        Args:
            file_path: Chemin vers le fichier TXT
            encoding: Encodage à utiliser
            
        Returns:
            Dictionnaire contenant le texte extrait et les métadonnées
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            
            file_stats = Path(file_path).stat()
            metadata = {
                "file_path": file_path,
                "encoding": encoding,
                "file_size_bytes": file_stats.st_size,
                "total_characters": len(content),
                "total_lines": len(content.splitlines()),
                "loader": "txt",
                "forced_encoding": True
            }
            
            logger.info(f"TXT chargé avec encodage {encoding}: {metadata['total_lines']} lignes")
            
            return {
                "text": content,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du TXT avec encodage {encoding}: {str(e)}")
            return {
                "text": "",
                "metadata": {
                    "error": str(e),
                    "file_path": file_path,
                    "encoding": encoding,
                    "total_characters": 0,
                    "total_lines": 0
                }
            }
    
    @staticmethod
    def is_valid_txt(file_path: str) -> bool:
        """
        Vérifie si un fichier peut être lu comme un fichier texte.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            True si le fichier peut être lu comme texte
        """
        try:
            # Essayer de lire les premiers bytes pour vérifier si c'est du texte
            with open(file_path, 'rb') as file:
                sample = file.read(1024)
            
            # Vérifier s'il y a des caractères de contrôle non-texte
            # (en excluant les caractères de saut de ligne normaux)
            text_characters = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            return bool(sample.translate(None, text_characters) == b'')
            
        except Exception:
            return False