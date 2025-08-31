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
Vous êtes un assistant IA spécialisé dans la génération de documents avec l'architecture 3+1. Votre tâche est d'analyser une transformation (Document Ancien → Document Exemple) et d'appliquer cette même transformation sur un nouveau document source.

Méthodologie:
1. **ANALYSER** : Comprenez comment le Document Ancien a été transformé en Document Exemple
2. **IDENTIFIER** : Repérez les patterns de transformation (style, structure, ton, format)
3. **APPLIQUER** : Utilisez ces mêmes patterns pour transformer le Nouveau Document Source
4. **GÉNÉRER** : Créez un document Markdown cohérent suivant la transformation identifiée

Instructions importantes:
- Respectez fidèlement le pattern de transformation observé
- Générez un document au format Markdown bien structuré
- Préservez les éléments de mise en forme appropriés
- Assurez-vous que le résultat soit cohérent et professionnel
- Intégrez les instructions utilisateur si fournies
"""
        
        self.transformation_prompt_template = """
## ANALYSE DE TRANSFORMATION

### DOCUMENT SOURCE ANCIEN (Référence originale):
{old_source_content}

### DOCUMENT EXEMPLE CONSTRUIT (Transformation appliquée):
{example_content}

### NOUVEAU DOCUMENT SOURCE (À transformer):
{new_source_content}

## INSTRUCTIONS

Analysez comment le Document Source Ancien a été transformé en Document Exemple Construit, puis appliquez cette même transformation au Nouveau Document Source.

{user_instructions}

## GÉNÉRATION DEMANDÉE:
Générez maintenant un nouveau document au format Markdown en appliquant la même transformation que celle observée entre le Document Source Ancien et le Document Exemple Construit.

Le document généré doit :
- Suivre le même pattern de transformation
- Être cohérent et bien structuré
- Respecter le format Markdown
- Intégrer les instructions utilisateur si fournies
"""
    
    def build_transformation_prompt(self, 
                                   old_source_documents: List[Dict[str, Any]],
                                   example_documents: List[Dict[str, Any]],
                                   new_source_documents: List[Dict[str, Any]],
                                   user_description: Optional[str] = None) -> Dict[str, Any]:
        """
        Construit un prompt pour la transformation 3+1.
        
        Args:
            old_source_documents: Documents sources anciens (référence)
            example_documents: Documents exemples construits (transformation)
            new_source_documents: Nouveaux documents sources (à traiter)
            user_description: Description optionnelle de l'utilisateur
            
        Returns:
            Dictionnaire contenant le prompt et les métadonnées
        """
        try:
            # Préparer le contenu des 3 types de documents
            old_source_content = self._prepare_source_content(old_source_documents)
            example_content = self._prepare_example_content(example_documents)
            new_source_content = self._prepare_source_content(new_source_documents)
            
            # Préparer les instructions utilisateur
            user_instructions = ""
            if user_description and user_description.strip():
                user_instructions = f"### INSTRUCTIONS UTILISATEUR:\n{user_description.strip()}\n"
            
            # Construire le prompt utilisateur
            user_prompt = self.transformation_prompt_template.format(
                old_source_content=old_source_content,
                example_content=example_content,
                new_source_content=new_source_content,
                user_instructions=user_instructions
            )
            
            # Vérifier la longueur du prompt
            total_length = len(self.system_prompt) + len(user_prompt)
            
            if total_length > self.max_context_length:
                logger.warning(f"Prompt trop long ({total_length} caractères), troncature nécessaire")
                user_prompt = self._truncate_transformation_prompt(
                    user_prompt, old_source_content, example_content, new_source_content
                )
            
            # Métadonnées du prompt
            prompt_metadata = {
                "total_length": len(self.system_prompt) + len(user_prompt),
                "system_prompt_length": len(self.system_prompt),
                "user_prompt_length": len(user_prompt),
                "old_source_documents_count": len(old_source_documents),
                "example_documents_count": len(example_documents),
                "new_source_documents_count": len(new_source_documents),
                "created_at": datetime.now().isoformat(),
                "language": self.language,
                "truncated": total_length > self.max_context_length,
                "user_description": user_description
            }
            
            logger.info(f"Prompt construit: {prompt_metadata['total_length']} caractères, {prompt_metadata['old_source_documents_count']} anciennes sources, {prompt_metadata['example_documents_count']} exemples, {prompt_metadata['new_source_documents_count']} nouvelles sources")
            
            return {
                "system_prompt": self.system_prompt,
                "user_prompt": user_prompt,
                "metadata": prompt_metadata
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la construction du prompt de transformation: {str(e)}")
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
    
    def _truncate_transformation_prompt(self, user_prompt: str, old_source_content: str, 
                                       example_content: str, new_source_content: str) -> str:
        """
        Tronque le prompt de transformation si nécessaire.
        
        Args:
            user_prompt: Prompt utilisateur complet
            old_source_content: Contenu des sources anciennes
            example_content: Contenu des exemples
            new_source_content: Contenu des nouvelles sources
            
        Returns:
            Prompt tronqué
        """
        try:
            # Calculer l'espace disponible
            available_space = self.max_context_length - len(self.system_prompt) - 500
            
            if len(user_prompt) <= available_space:
                return user_prompt
            
            # Stratégie de troncature: réduire proportionnellement les 3 contenus
            total_content = len(old_source_content) + len(example_content) + len(new_source_content)
            
            if total_content == 0:
                return user_prompt[:available_space]
            
            old_ratio = len(old_source_content) / total_content
            example_ratio = len(example_content) / total_content
            new_ratio = len(new_source_content) / total_content
            
            # Calculer les nouvelles tailles
            content_space = available_space - 1000  # Espace pour le template
            new_old_length = int(content_space * old_ratio)
            new_example_length = int(content_space * example_ratio)
            new_new_length = int(content_space * new_ratio)
            
            # Tronquer les contenus
            truncated_old = old_source_content[:new_old_length] + "\n[...tronqué...]" if len(old_source_content) > new_old_length else old_source_content
            truncated_example = example_content[:new_example_length] + "\n[...tronqué...]" if len(example_content) > new_example_length else example_content
            truncated_new = new_source_content[:new_new_length] + "\n[...tronqué...]" if len(new_source_content) > new_new_length else new_source_content
            
            # Reconstruire le prompt avec le contenu tronqué
            truncated_prompt = self.transformation_prompt_template.format(
                old_source_content=truncated_old,
                example_content=truncated_example,
                new_source_content=truncated_new,
                user_instructions=""
            )
            
            logger.info(f"Prompt tronqué de {len(user_prompt)} à {len(truncated_prompt)} caractères")
            return truncated_prompt
            
        except Exception as e:
            logger.error(f"Erreur lors de la troncature: {str(e)}")
            return user_prompt[:available_space]
    
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