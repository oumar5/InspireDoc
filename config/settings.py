import os
from typing import Dict, Any

class Settings:
    """
    Configuration centralisée pour l'application InspireDoc.
    """
    
    # Configuration LLM
    GPT4O_API_KEY = os.getenv("GPT4O_API_KEY")
    GPT4O_ENDPOINT = os.getenv("GPT4O_ENDPOINT")
    
    # Configuration des fichiers
    UPLOAD_DIR = "data/uploads"
    PROCESSED_DIR = "data/processed"
    EXPORTS_DIR = "data/exports"
    
    # Formats supportés
    SUPPORTED_FORMATS = ["pdf", "txt", "docx"]
    
    # Configuration LLM par défaut
    DEFAULT_LLM_CONFIG = {
        "temperature": 0.3,
        "top_p": 1,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }
    
    # Taille maximale des fichiers (en MB)
    MAX_FILE_SIZE_MB = 10
    
    # Configuration Streamlit
    STREAMLIT_CONFIG = {
        "page_title": "InspireDoc",
        "page_icon": "📝",
        "layout": "wide"
    }
    
    @classmethod
    def get_upload_path(cls) -> str:
        """Retourne le chemin absolu du dossier d'upload."""
        return os.path.abspath(cls.UPLOAD_DIR)
    
    @classmethod
    def get_processed_path(cls) -> str:
        """Retourne le chemin absolu du dossier de traitement."""
        return os.path.abspath(cls.PROCESSED_DIR)
    
    @classmethod
    def get_exports_path(cls) -> str:
        """Retourne le chemin absolu du dossier d'export."""
        return os.path.abspath(cls.EXPORTS_DIR)
    
    @classmethod
    def validate_config(cls) -> bool:
        """Valide la configuration nécessaire."""
        if not cls.GPT4O_API_KEY or not cls.GPT4O_ENDPOINT:
            return False
        return True