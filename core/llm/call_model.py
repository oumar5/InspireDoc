import os
import json
import logging
import requests
from typing import Optional, List, Dict, Tuple, Any
from datetime import datetime

from config.settings import Settings

logger = logging.getLogger(__name__)

class LLMCaller:
    """
    Classe pour appeler les modèles de langage (GPT-4o et autres).
    Inspirée du CustomGPT4oLLM existant mais adaptée pour InspireDoc.
    """
    
    def __init__(self, 
                 api_key: str = None, 
                 endpoint: str = None,
                 model_name: str = "gpt-4o",
                 default_config: Dict[str, Any] = None):
        """
        Initialise le caller LLM.
        
        Args:
            api_key: Clé API (ou depuis les variables d'environnement)
            endpoint: Endpoint API (ou depuis les variables d'environnement)
            model_name: Nom du modèle à utiliser
            default_config: Configuration par défaut du modèle
        """
        self.api_key = api_key or Settings.GPT4O_API_KEY
        self.endpoint = endpoint or Settings.GPT4O_ENDPOINT
        self.model_name = model_name
        
        # Configuration par défaut depuis Settings
        self.default_config = default_config or Settings.DEFAULT_LLM_CONFIG.copy()
        
        if not self.api_key or not self.endpoint:
            raise ValueError("❌ API Key ou endpoint GPT-4o non définis.")
        
        logger.info(f"✅ LLM configuré: {self.model_name} avec endpoint {self.endpoint}")
    
    def call_model(self, 
                   system_prompt: str,
                   user_prompt: str,
                   config: Optional[Dict[str, Any]] = None,
                   user_id: str = "inspiredoc-user") -> Dict[str, Any]:
        """
        Appelle le modèle de langage avec les prompts fournis.
        
        Args:
            system_prompt: Prompt système
            user_prompt: Prompt utilisateur
            config: Configuration spécifique pour cet appel
            user_id: Identifiant utilisateur
            
        Returns:
            Dictionnaire avec la réponse et les métadonnées
        """
        try:
            # Fusionner la configuration
            call_config = {**self.default_config}
            if config:
                call_config.update(config)
            
            # Construire l'URL
            url = f"{self.endpoint}/deployments/{self.model_name}/chat/completions?api-version=2024-06-01"
            
            # Headers
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Payload
            payload = {
                **call_config,
                "stream": False,
                "user": user_id,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "n": 1
            }
            
            # Métadonnées de l'appel
            call_metadata = {
                "timestamp": datetime.now().isoformat(),
                "model": self.model_name,
                "config": call_config,
                "prompt_length": len(system_prompt) + len(user_prompt),
                "user_id": user_id
            }
            
            logger.info(f"🔄 Appel LLM: {call_metadata['prompt_length']} caractères, config: {call_config}")
            
            # Appel API
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            # Traitement de la réponse
            data = response.json()
            
            if "choices" not in data or not data["choices"]:
                raise ValueError("Réponse API invalide: pas de choix disponibles")
            
            generated_content = data["choices"][0]["message"]["content"]
            
            # Métadonnées de la réponse
            response_metadata = {
                **call_metadata,
                "success": True,
                "response_length": len(generated_content),
                "usage": data.get("usage", {}),
                "finish_reason": data["choices"][0].get("finish_reason"),
                "response_time": (datetime.now() - datetime.fromisoformat(call_metadata["timestamp"])).total_seconds()
            }
            
            logger.info(f"✅ Réponse LLM reçue: {response_metadata['response_length']} caractères, usage: {response_metadata['usage']}")
            
            return {
                "success": True,
                "content": generated_content,
                "metadata": response_metadata,
                "raw_response": data
            }
            
        except requests.exceptions.HTTPError as http_err:
            error_message = f"Erreur HTTP API {self.model_name}: {response.status_code}"
            if hasattr(response, 'text'):
                error_message += f", {response.text}"
            
            logger.error(error_message)
            
            return {
                "success": False,
                "content": "",
                "error": error_message,
                "metadata": {
                    **call_metadata,
                    "success": False,
                    "error_type": "http_error",
                    "status_code": response.status_code if 'response' in locals() else None
                }
            }
            
        except requests.exceptions.Timeout:
            error_message = f"Timeout lors de l'appel API {self.model_name}"
            logger.error(error_message)
            
            return {
                "success": False,
                "content": "",
                "error": error_message,
                "metadata": {
                    **call_metadata,
                    "success": False,
                    "error_type": "timeout"
                }
            }
            
        except Exception as e:
            error_message = f"Exception lors de l'appel API {self.model_name}: {str(e)}"
            logger.error(error_message)
            
            return {
                "success": False,
                "content": "",
                "error": error_message,
                "metadata": {
                    **call_metadata,
                    "success": False,
                    "error_type": "general_exception",
                    "exception": str(e)
                }
            }
    
    def call_with_prompt_data(self, prompt_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Appelle le modèle avec des données de prompt structurées.
        
        Args:
            prompt_data: Données de prompt du PromptBuilder
            **kwargs: Arguments supplémentaires pour l'appel
            
        Returns:
            Dictionnaire avec la réponse et les métadonnées
        """
        if "system_prompt" not in prompt_data or "user_prompt" not in prompt_data:
            raise ValueError("Données de prompt invalides: system_prompt et user_prompt requis")
        
        return self.call_model(
            system_prompt=prompt_data["system_prompt"],
            user_prompt=prompt_data["user_prompt"],
            **kwargs
        )
    
    def generate_document(self, 
                         prompt_data: Dict[str, Any],
                         generation_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Génère un document avec une configuration optimisée.
        
        Args:
            prompt_data: Données de prompt du PromptBuilder
            generation_config: Configuration spécifique pour la génération
            
        Returns:
            Dictionnaire avec le document généré et les métadonnées
        """
        # Configuration optimisée pour la génération de documents
        doc_config = {
            "temperature": 0.3,  # Créativité modérée
            "top_p": 0.9,       # Diversité contrôlée
            "max_tokens": 3000, # Plus de tokens pour les documents longs
            "presence_penalty": 0.1,  # Éviter les répétitions
            "frequency_penalty": 0.1  # Encourager la variété
        }
        
        if generation_config:
            doc_config.update(generation_config)
        
        result = self.call_with_prompt_data(prompt_data, config=doc_config)
        
        if result["success"]:
            # Post-traitement du document généré
            generated_content = result["content"]
            
            # Validation basique du Markdown
            if not self._validate_markdown(generated_content):
                logger.warning("Le contenu généré ne semble pas être du Markdown valide")
            
            # Ajout de métadonnées spécifiques au document
            result["metadata"]["document_type"] = "markdown"
            result["metadata"]["word_count"] = len(generated_content.split())
            result["metadata"]["line_count"] = len(generated_content.splitlines())
        
        return result
    
    def _validate_markdown(self, content: str) -> bool:
        """
        Validation basique du contenu Markdown.
        
        Args:
            content: Contenu à valider
            
        Returns:
            True si le contenu semble être du Markdown valide
        """
        if not content.strip():
            return False
        
        # Vérifications basiques
        markdown_indicators = [
            content.count('#') > 0,  # Titres
            content.count('*') > 0 or content.count('_') > 0,  # Emphase
            content.count('-') > 2 or content.count('*') > 2,  # Listes
            '\n\n' in content  # Paragraphes
        ]
        
        return any(markdown_indicators)
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API.
        
        Returns:
            True si la connexion fonctionne
        """
        try:
            test_result = self.call_model(
                system_prompt="Vous êtes un assistant de test.",
                user_prompt="Répondez simplement 'OK' pour confirmer que vous fonctionnez.",
                config={"max_tokens": 10}
            )
            
            return test_result["success"]
            
        except Exception as e:
            logger.error(f"Erreur lors du test de connexion: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retourne les informations sur le modèle configuré.
        
        Returns:
            Dictionnaire avec les informations du modèle
        """
        return {
            "model_name": self.model_name,
            "endpoint": self.endpoint,
            "has_api_key": bool(self.api_key),
            "default_config": self.default_config,
            "connection_tested": self.test_connection()
        }