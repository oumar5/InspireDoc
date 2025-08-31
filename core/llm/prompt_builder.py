import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PromptBuilder:
    """
    Classe pour construire des prompts structurés pour la génération de documents.
    """
    
    def __init__(self, 
                 max_context_length: int = 8000,
                 include_metadata: bool = True,
                 language: str = "français"):
        """
        Initialise le constructeur de prompts.
        
        Args:
            max_context_length: Longueur maximale du contexte en caractères
            include_metadata: Inclure les métadonnées dans le prompt
            language: Langue pour les instructions
        """
        self.max_context_length = max_context_length
        self.include_metadata = include_metadata
        self.language = language
        
        self._init_templates()
    
    def _init_templates(self):
        """
        Initialise les templates de prompts.
        """
        self.system_prompt = """
Vous êtes un assistant IA spécialisé dans la génération de documents. Votre tâche est de créer un nouveau document au format Markdown en vous inspirant du style et de la structure d'un document exemple, tout en utilisant le contenu des documents sources fournis.

Instructions importantes:
1. Respectez le style, la structure et le format du document exemple
2. Utilisez uniquement les informations des documents sources pour le contenu
3. Générez un document cohérent et bien structuré en Markdown
4. Préservez les éléments de mise en forme (titres, listes, tableaux, etc.)
5. Assurez-vous que le document généré soit complet et professionnel
6. Ne mentionnez pas les documents sources dans le contenu généré
"""
        
        self.user_prompt_template = """
## DOCUMENT EXEMPLE (Style et structure à respecter):
{example_content}

## DOCUMENTS SOURCES (Contenu à utiliser):
{source_content}

## DEMANDE DE GÉNÉRATION:
{generation_request}

## INSTRUCTIONS SPÉCIFIQUES:
- Format de sortie: Markdown uniquement
- Longueur approximative: {target_length}
- Style: Suivre exactement le document exemple
- Contenu: Basé sur les documents sources

Générez maintenant le document demandé:
"""
    
    def build_prompt(self, 
                    source_documents: List[Dict[str, Any]],
                    example_documents: List[Dict[str, Any]],
                    generation_request: str,
                    target_length: str = "similaire à l'exemple",
                    additional_instructions: Optional[str] = None) -> Dict[str, Any]:
        """
        Construit un prompt complet pour la génération de document.
        
        Args:
            source_documents: Liste des documents sources
            example_documents: Liste des documents exemples
            generation_request: Demande spécifique de génération
            target_length: Longueur cible du document
            additional_instructions: Instructions supplémentaires
            
        Returns:
            Dictionnaire contenant le prompt et les métadonnées
        """
        try:
            # Préparer le contenu des sources
            source_content = self._prepare_source_content(source_documents)
            
            # Préparer le contenu des exemples
            example_content = self._prepare_example_content(example_documents)
            
            # Construire le prompt utilisateur
            user_prompt = self.user_prompt_template.format(
                example_content=example_content,
                source_content=source_content,
                generation_request=generation_request,
                target_length=target_length
            )
            
            # Ajouter les instructions supplémentaires si fournies
            if additional_instructions:
                user_prompt += f"\n\n## INSTRUCTIONS SUPPLÉMENTAIRES:\n{additional_instructions}"
            
            # Vérifier la longueur du prompt
            total_length = len(self.system_prompt) + len(user_prompt)
            
            if total_length > self.max_context_length:
                logger.warning(f"Prompt trop long ({total_length} caractères), troncature nécessaire")
                user_prompt = self._truncate_prompt(user_prompt, source_content, example_content)
            
            # Métadonnées du prompt
            prompt_metadata = {
                "total_length": len(self.system_prompt) + len(user_prompt),
                "system_prompt_length": len(self.system_prompt),
                "user_prompt_length": len(user_prompt),
                "source_documents_count": len(source_documents),
                "example_documents_count": len(example_documents),
                "created_at": datetime.now().isoformat(),
                "language": self.language,
                "truncated": total_length > self.max_context_length
            }
            
            logger.info(f"Prompt construit: {prompt_metadata['total_length']} caractères, {prompt_metadata['source_documents_count']} sources, {prompt_metadata['example_documents_count']} exemples")
            
            return {
                "system_prompt": self.system_prompt,
                "user_prompt": user_prompt,
                "metadata": prompt_metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la construction du prompt: {str(e)}")
            raise
    
    def _prepare_source_content(self, source_documents: List[Dict[str, Any]]) -> str:
        """
        Prépare le contenu des documents sources.
        
        Args:
            source_documents: Liste des documents sources
            
        Returns:
            Contenu formaté des sources
        """
        if not source_documents:
            return "Aucun document source fourni."
        
        formatted_sources = []
        
        for i, doc in enumerate(source_documents, 1):
            content = doc.get('text', '')
            metadata = doc.get('metadata', {})
            
            source_header = f"### Source {i}"
            
            if self.include_metadata and metadata:
                file_path = metadata.get('file_path', 'Inconnu')
                source_header += f" ({file_path})"
            
            source_header += ":\n"
            
            # Limiter la longueur de chaque source
            max_source_length = self.max_context_length // (len(source_documents) * 2)
            if len(content) > max_source_length:
                content = content[:max_source_length] + "\n[...contenu tronqué...]"
            
            formatted_sources.append(source_header + content)
        
        return "\n\n".join(formatted_sources)
    
    def _prepare_example_content(self, example_documents: List[Dict[str, Any]]) -> str:
        """
        Prépare le contenu des documents exemples.
        
        Args:
            example_documents: Liste des documents exemples
            
        Returns:
            Contenu formaté des exemples
        """
        if not example_documents:
            return "Aucun document exemple fourni."
        
        formatted_examples = []
        
        for i, doc in enumerate(example_documents, 1):
            content = doc.get('text', '')
            metadata = doc.get('metadata', {})
            
            example_header = f"### Exemple {i}"
            
            if self.include_metadata and metadata:
                file_path = metadata.get('file_path', 'Inconnu')
                example_header += f" ({file_path})"
            
            example_header += ":\n"
            
            # Limiter la longueur de chaque exemple
            max_example_length = self.max_context_length // (len(example_documents) * 3)
            if len(content) > max_example_length:
                content = content[:max_example_length] + "\n[...contenu tronqué...]"
            
            formatted_examples.append(example_header + content)
        
        return "\n\n".join(formatted_examples)
    
    def _truncate_prompt(self, user_prompt: str, source_content: str, example_content: str) -> str:
        """
        Tronque le prompt s'il est trop long.
        
        Args:
            user_prompt: Prompt utilisateur original
            source_content: Contenu des sources
            example_content: Contenu des exemples
            
        Returns:
            Prompt tronqué
        """
        available_length = self.max_context_length - len(self.system_prompt) - 500  # Marge de sécurité
        
        # Répartir l'espace disponible: 40% pour les exemples, 50% pour les sources, 10% pour le reste
        example_max = int(available_length * 0.4)
        source_max = int(available_length * 0.5)
        
        # Tronquer le contenu des exemples
        if len(example_content) > example_max:
            example_content = example_content[:example_max] + "\n[...contenu tronqué...]"
        
        # Tronquer le contenu des sources
        if len(source_content) > source_max:
            source_content = source_content[:source_max] + "\n[...contenu tronqué...]"
        
        # Reconstruire le prompt avec le contenu tronqué
        truncated_prompt = self.user_prompt_template.format(
            example_content=example_content,
            source_content=source_content,
            generation_request="[Demande de génération maintenue]",
            target_length="similaire à l'exemple"
        )
        
        return truncated_prompt
    
    def build_simple_prompt(self, content: str, task: str) -> Dict[str, Any]:
        """
        Construit un prompt simple pour des tâches basiques.
        
        Args:
            content: Contenu à traiter
            task: Tâche à effectuer
            
        Returns:
            Dictionnaire contenant le prompt simple
        """
        simple_system = "Vous êtes un assistant IA spécialisé dans le traitement de documents."
        
        simple_user = f"""
Tâche: {task}

Contenu:
{content}

Veuillez traiter ce contenu selon la tâche demandée.
"""
        
        return {
            "system_prompt": simple_system,
            "user_prompt": simple_user,
            "metadata": {
                "total_length": len(simple_system) + len(simple_user),
                "type": "simple",
                "created_at": datetime.now().isoformat()
            }
        }
    
    def validate_prompt(self, prompt_data: Dict[str, Any]) -> bool:
        """
        Valide un prompt construit.
        
        Args:
            prompt_data: Données du prompt à valider
            
        Returns:
            True si le prompt est valide
        """
        required_keys = ['system_prompt', 'user_prompt', 'metadata']
        
        for key in required_keys:
            if key not in prompt_data:
                logger.error(f"Clé manquante dans le prompt: {key}")
                return False
        
        if not prompt_data['system_prompt'] or not prompt_data['user_prompt']:
            logger.error("Prompt système ou utilisateur vide")
            return False
        
        total_length = prompt_data['metadata'].get('total_length', 0)
        if total_length > self.max_context_length:
            logger.warning(f"Prompt très long: {total_length} caractères")
        
        return True