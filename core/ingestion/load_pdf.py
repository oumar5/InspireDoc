import logging
from typing import Optional, Dict, Any
from pathlib import Path

try:
    import pypdf
except ImportError:
    try:
        import pdfplumber
    except ImportError:
        raise ImportError("Veuillez installer pypdf ou pdfplumber: pip install pypdf pdfplumber")

logger = logging.getLogger(__name__)

class PDFLoader:
    """
    Classe pour charger et extraire le texte des fichiers PDF.
    """
    
    def __init__(self, use_pdfplumber: bool = True):
        """
        Initialise le loader PDF.
        
        Args:
            use_pdfplumber: Si True, utilise pdfplumber, sinon pypdf
        """
        self.use_pdfplumber = use_pdfplumber
        
    def load(self, file_path: str) -> Dict[str, Any]:
        """
        Charge un fichier PDF et extrait son contenu.
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire contenant le texte extrait et les métadonnées
        """
        try:
            if self.use_pdfplumber:
                return self._load_with_pdfplumber(file_path)
            else:
                return self._load_with_pypdf(file_path)
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement du PDF {file_path}: {str(e)}")
            return {
                "text": "",
                "metadata": {
                    "error": str(e),
                    "file_path": file_path,
                    "pages": 0
                }
            }
    
    def _load_with_pdfplumber(self, file_path: str) -> Dict[str, Any]:
        """
        Charge un PDF avec pdfplumber.
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire avec le texte et les métadonnées
        """
        import pdfplumber
        
        text_content = []
        metadata = {
            "file_path": file_path,
            "pages": 0,
            "loader": "pdfplumber"
        }
        
        with pdfplumber.open(file_path) as pdf:
            metadata["pages"] = len(pdf.pages)
            
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                        logger.debug(f"Page {page_num}: {len(page_text)} caractères extraits")
                except Exception as e:
                    logger.warning(f"Erreur extraction page {page_num}: {str(e)}")
                    continue
        
        full_text = "\n\n".join(text_content)
        metadata["total_characters"] = len(full_text)
        
        logger.info(f"PDF chargé: {metadata['pages']} pages, {metadata['total_characters']} caractères")
        
        return {
            "text": full_text,
            "metadata": metadata
        }
    
    def _load_with_pypdf(self, file_path: str) -> Dict[str, Any]:
        """
        Charge un PDF avec pypdf.
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire avec le texte et les métadonnées
        """
        import pypdf
        
        text_content = []
        metadata = {
            "file_path": file_path,
            "pages": 0,
            "loader": "pypdf"
        }
        
        with open(file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            metadata["pages"] = len(pdf_reader.pages)
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                        logger.debug(f"Page {page_num}: {len(page_text)} caractères extraits")
                except Exception as e:
                    logger.warning(f"Erreur extraction page {page_num}: {str(e)}")
                    continue
        
        full_text = "\n\n".join(text_content)
        metadata["total_characters"] = len(full_text)
        
        logger.info(f"PDF chargé: {metadata['pages']} pages, {metadata['total_characters']} caractères")
        
        return {
            "text": full_text,
            "metadata": metadata
        }
    
    @staticmethod
    def is_valid_pdf(file_path: str) -> bool:
        """
        Vérifie si un fichier est un PDF valide.
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            True si le fichier est un PDF valide
        """
        try:
            with open(file_path, 'rb') as file:
                header = file.read(4)
                return header == b'%PDF'
        except Exception:
            return False