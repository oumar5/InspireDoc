import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

try:
    import markdown
except ImportError:
    raise ImportError("Veuillez installer markdown: pip install markdown")

try:
    import weasyprint
except ImportError:
    try:
        import pdfkit
    except ImportError:
        raise ImportError("Veuillez installer weasyprint ou pdfkit: pip install weasyprint pdfkit")

logger = logging.getLogger(__name__)

class MarkdownToPDFConverter:
    """
    Convertisseur Markdown vers PDF avec support de styles personnalisés.
    """
    
    def __init__(self, use_weasyprint: bool = True):
        """
        Initialise le convertisseur.
        
        Args:
            use_weasyprint: Utiliser WeasyPrint (True) ou pdfkit (False)
        """
        self.use_weasyprint = use_weasyprint
        self._init_css_styles()
        
        # Vérifier la disponibilité des outils
        if self.use_weasyprint:
            try:
                import weasyprint
                self.converter_available = True
            except ImportError:
                logger.warning("WeasyPrint non disponible, basculement vers pdfkit")
                self.use_weasyprint = False
                try:
                    import pdfkit
                    self.converter_available = True
                except ImportError:
                    self.converter_available = False
                    logger.error("Aucun convertisseur PDF disponible")
        else:
            try:
                import pdfkit
                self.converter_available = True
            except ImportError:
                self.converter_available = False
                logger.error("pdfkit non disponible")
    
    def _init_css_styles(self):
        """
        Initialise les styles CSS pour le PDF.
        """
        self.default_css = """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: bold;
        }
        
        h1 {
            font-size: 24pt;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.3em;
        }
        
        h2 {
            font-size: 20pt;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 0.2em;
        }
        
        h3 {
            font-size: 16pt;
        }
        
        h4 {
            font-size: 14pt;
        }
        
        p {
            margin-bottom: 1em;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 1em;
            padding-left: 2em;
        }
        
        li {
            margin-bottom: 0.3em;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 1em 0;
            padding: 0.5em 1em;
            background-color: #f8f9fa;
            font-style: italic;
        }
        
        code {
            background-color: #f1f2f6;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        
        pre {
            background-color: #f1f2f6;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            margin: 1em 0;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 0.5em;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        .page-break {
            page-break-before: always;
        }
        
        .no-break {
            page-break-inside: avoid;
        }
        """
    
    def convert(self, 
                markdown_content: str,
                output_path: str,
                custom_css: Optional[str] = None,
                metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Convertit du contenu Markdown en PDF.
        
        Args:
            markdown_content: Contenu Markdown à convertir
            output_path: Chemin de sortie pour le PDF
            custom_css: CSS personnalisé optionnel
            metadata: Métadonnées du document
            
        Returns:
            Dictionnaire avec le résultat de la conversion
        """
        if not self.converter_available:
            raise RuntimeError("Aucun convertisseur PDF disponible")
        
        try:
            # Conversion Markdown vers HTML
            html_content = self._markdown_to_html(markdown_content, metadata)
            
            # Application des styles CSS
            css_styles = custom_css or self.default_css
            
            # Conversion selon l'outil disponible
            if self.use_weasyprint:
                result = self._convert_with_weasyprint(html_content, css_styles, output_path)
            else:
                result = self._convert_with_pdfkit(html_content, css_styles, output_path)
            
            # Métadonnées de conversion
            conversion_metadata = {
                'converted_at': datetime.now().isoformat(),
                'converter_used': 'weasyprint' if self.use_weasyprint else 'pdfkit',
                'output_path': output_path,
                'file_size': os.path.getsize(output_path) if os.path.exists(output_path) else 0,
                'markdown_length': len(markdown_content),
                'html_length': len(html_content)
            }
            
            if metadata:
                conversion_metadata['document_metadata'] = metadata
            
            logger.info(f"PDF généré avec succès: {output_path} ({conversion_metadata['file_size']} bytes)")
            
            return {
                'success': True,
                'output_path': output_path,
                'metadata': conversion_metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'output_path': output_path
            }
    
    def _markdown_to_html(self, markdown_content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Convertit le Markdown en HTML.
        
        Args:
            markdown_content: Contenu Markdown
            metadata: Métadonnées optionnelles
            
        Returns:
            Contenu HTML
        """
        # Configuration des extensions Markdown
        extensions = [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ]
        
        # Conversion Markdown vers HTML
        md = markdown.Markdown(extensions=extensions)
        html_body = md.convert(markdown_content)
        
        # Construction du HTML complet
        title = "Document InspireDoc"
        if metadata and 'title' in metadata:
            title = metadata['title']
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        return html_content
    
    def _convert_with_weasyprint(self, html_content: str, css_styles: str, output_path: str) -> bool:
        """
        Convertit avec WeasyPrint.
        
        Args:
            html_content: Contenu HTML
            css_styles: Styles CSS
            output_path: Chemin de sortie
            
        Returns:
            True si succès
        """
        import weasyprint
        
        # Créer le document HTML avec CSS
        html_doc = weasyprint.HTML(string=html_content)
        css_doc = weasyprint.CSS(string=css_styles)
        
        # Générer le PDF
        html_doc.write_pdf(output_path, stylesheets=[css_doc])
        
        return True
    
    def _convert_with_pdfkit(self, html_content: str, css_styles: str, output_path: str) -> bool:
        """
        Convertit avec pdfkit.
        
        Args:
            html_content: Contenu HTML
            css_styles: Styles CSS
            output_path: Chemin de sortie
            
        Returns:
            True si succès
        """
        import pdfkit
        
        # Injecter le CSS dans le HTML
        html_with_css = html_content.replace(
            '</head>',
            f'<style>{css_styles}</style></head>'
        )
        
        # Options pour pdfkit
        options = {
            'page-size': 'A4',
            'margin-top': '2cm',
            'margin-right': '2cm',
            'margin-bottom': '2cm',
            'margin-left': '2cm',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Générer le PDF
        pdfkit.from_string(html_with_css, output_path, options=options)
        
        return True
    
    def convert_file(self, 
                    markdown_file_path: str,
                    output_path: Optional[str] = None,
                    custom_css: Optional[str] = None) -> Dict[str, Any]:
        """
        Convertit un fichier Markdown en PDF.
        
        Args:
            markdown_file_path: Chemin vers le fichier Markdown
            output_path: Chemin de sortie (optionnel)
            custom_css: CSS personnalisé
            
        Returns:
            Dictionnaire avec le résultat de la conversion
        """
        try:
            # Lire le fichier Markdown
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Générer le chemin de sortie si non fourni
            if not output_path:
                input_path = Path(markdown_file_path)
                output_path = str(input_path.with_suffix('.pdf'))
            
            # Métadonnées du fichier
            file_metadata = {
                'source_file': markdown_file_path,
                'file_size': os.path.getsize(markdown_file_path)
            }
            
            return self.convert(markdown_content, output_path, custom_css, file_metadata)
            
        except Exception as e:
            logger.error(f"Erreur lors de la conversion du fichier {markdown_file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'source_file': markdown_file_path
            }
    
    def is_available(self) -> bool:
        """
        Vérifie si le convertisseur est disponible.
        
        Returns:
            True si un convertisseur est disponible
        """
        return self.converter_available
    
    def get_converter_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur le convertisseur.
        
        Returns:
            Dictionnaire avec les informations
        """
        return {
            'available': self.converter_available,
            'preferred_converter': 'weasyprint' if self.use_weasyprint else 'pdfkit',
            'weasyprint_available': 'weasyprint' in globals(),
            'pdfkit_available': 'pdfkit' in globals()
        }