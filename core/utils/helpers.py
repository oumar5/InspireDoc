import os
import uuid
import hashlib
from typing import List, Optional
from datetime import datetime

def generate_unique_filename(original_filename: str) -> str:
    """
    Génère un nom de fichier unique basé sur le timestamp et un UUID.
    
    Args:
        original_filename: Le nom de fichier original
        
    Returns:
        Un nom de fichier unique
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}_{unique_id}{ext}"

def get_file_hash(file_path: str) -> str:
    """
    Calcule le hash MD5 d'un fichier.
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        Hash MD5 du fichier
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Valide l'extension d'un fichier.
    
    Args:
        filename: Nom du fichier
        allowed_extensions: Liste des extensions autorisées
        
    Returns:
        True si l'extension est valide, False sinon
    """
    if not filename:
        return False
    
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    return ext in [e.lower() for e in allowed_extensions]

def ensure_directory_exists(directory_path: str) -> None:
    """
    S'assure qu'un répertoire existe, le crée si nécessaire.
    
    Args:
        directory_path: Chemin du répertoire
    """
    os.makedirs(directory_path, exist_ok=True)

def clean_filename(filename: str) -> str:
    """
    Nettoie un nom de fichier en supprimant les caractères non autorisés.
    
    Args:
        filename: Nom de fichier à nettoyer
        
    Returns:
        Nom de fichier nettoyé
    """
    # Caractères à remplacer par des underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Supprimer les espaces multiples et les remplacer par un seul underscore
    filename = '_'.join(filename.split())
    
    return filename

def format_file_size(size_bytes: int) -> str:
    """
    Formate la taille d'un fichier en unités lisibles.
    
    Args:
        size_bytes: Taille en bytes
        
    Returns:
        Taille formatée (ex: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Tronque un texte à une longueur maximale.
    
    Args:
        text: Texte à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué
        
    Returns:
        Texte tronqué
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix