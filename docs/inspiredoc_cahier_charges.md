# Cahier des charges - InspireDoc

## 1. Présentation du projet

**Nom du projet :** InspireDoc\
**Objectif :** Développer une application web (MVP avec Streamlit) permettant aux utilisateurs d’uploader des documents sources et exemples, puis de générer automatiquement un nouveau document inspiré au format Markdown, exportable en PDF ou DOCX, et affiché de façon lisible et designée, grâce à l’intelligence artificielle.

---

## 2. Objectifs fonctionnels

1. **Upload de documents :**

   - Formats supportés : PDF, TXT, DOCX.
   - Différenciation entre :
     - **Document source ancien** : Document de référence original
     - **Document exemple construit** : Exemple créé à partir de la source (style/structure)
     - **Nouveau document source** : Nouvelle source pour génération
   - **Upload multiple** : Plusieurs fichiers par type autorisés

2. **Extraction et nettoyage du contenu :**

   - Extraction automatique du texte brut depuis les fichiers.
   - Nettoyage : suppression des métadonnées, sauts de page, caractères spéciaux inutiles.
   - Normalisation du texte (minuscule, suppression d’espaces multiples, etc.).

3. **Préparation du prompt :**

   - Construction d’un prompt structuré avec :
     - Contexte (documents sources)
     - Exemple(s) de référence
     - Nouveau document (demande)

4. **Génération via LLM :**

   - **Architecture 3+1** :
     - **Document source ancien** → Contenu de référence
     - **Document exemple construit** → Style et structure cible
     - **Nouveau document source** → Nouvelle information à traiter
     - **Description utilisateur** → Prompt optionnel pour personnaliser
   - **Prompt intelligent** : Construction automatique basée sur les 3 documents
   - **Paramètres configurables** :
     - Température (créativité)
     - Longueur maximale
     - Style de génération
   - **Modèle IA** : GPT-4o via API Azure
   - **Gestion d'erreurs** : Retry automatique, fallback
   - Retour d'un document généré au format Markdown respectant le style de l'exemple et le contenu des sources.

5. **Affichage & Export :**

   - Affichage du Markdown généré directement dans Streamlit avec rendu visuel.
   - Export possible en PDF ou DOCX tout en conservant la mise en forme.

6. **Interface utilisateur :**

   - Application web Streamlit avec multi-pages :
     - Page d’accueil (home)
     - Page de génération (upload + résultat rendu Markdown)
     - Page paramètres (choix du modèle, temperature, etc.)
     - Page À propos

---

## 3. Objectifs non fonctionnels

- **Performance :** génération rapide (max 10s pour documents moyens).
- **Évolutivité :** possibilité d’ajouter une base vectorielle pour grands corpus.
- **Sécurité :** gestion sécurisée des fichiers temporaires.
- **Qualité du code :** architecture modulaire séparant métier et interface.
- **Tests unitaires :** ingestion, nettoyage, génération et rendu Markdown.

---

## 4. Architecture technique

### Langage & Frameworks

- Python 3.10+
- Streamlit (UI)
- Librairies :
  - `pypdf` ou `pdfplumber` (extraction PDF)
  - `python-docx` (lecture/export DOCX)
  - `markdown2` ou `mistune` (rendu Markdown)
  - `weasyprint` ou `pdfkit` (export PDF)
  - `re` et `nltk/spacy` (nettoyage texte)
  - `openai` ou `transformers` (modèles IA)

### Structure des dossiers (avec fichiers séparés pour modularité)

```
inspiredoc/
├── app.py
├── config/
│   ├── settings.py
├── data/
│   ├── uploads/                  # Fichiers uploadés
│   ├── processed/                # Textes nettoyés
│   ├── exports/                  # Documents générés (Markdown, PDF, DOCX)
├── core/
│   ├── ingestion/
│   │   ├── load_pdf.py
│   │   ├── load_txt.py
│   │   ├── load_docx.py
│   ├── preprocessing/
│   │   ├── clean_text.py
│   │   ├── normalize_text.py
│   ├── llm/
│   │   ├── prompt_builder.py
│   │   ├── call_model.py
│   ├── rendering/
│   │   ├── markdown_to_pdf.py
│   │   ├── markdown_to_docx.py
│   ├── services/
│   │   ├── document_service.py
│   ├── utils/
│       ├── helpers.py
├── pages/
│   ├── home.py
│   ├── generation.py
│   ├── settings.py
│   ├── about.py
├── tests/
│   ├── test_loaders.py
│   ├── test_cleaning.py
│   ├── test_prompt.py
│   ├── test_rendering.py
│   ├── test_document_service.py
```

---

## 5. Workflow du système

1. L’utilisateur charge les documents (source, exemple, nouveau).
2. Le système extrait le texte brut (fichiers séparés par type).
3. Le module de preprocessing nettoie et normalise le texte (fichiers séparés pour chaque tâche).
4. Le service métier (`document_service`) construit le prompt.
5. Le LLM génère le document Markdown.
6. Le module de rendu convertit le Markdown en PDF ou DOCX si nécessaire.
7. L’utilisateur visualise le document en Markdown rendu dans Streamlit et peut l’exporter.

---

## 6. Roadmap de développement

### Étape 1 - MVP (2-3 semaines)

- Upload de PDF/TXT.
- Extraction texte + nettoyage simple.
- Génération Markdown basique via GPT-4.
- Affichage du Markdown dans Streamlit.
- Export PDF simple.

### Étape 2 - Améliorations (1-2 mois)

- Support DOCX en entrée et sortie.
- Paramétrage avancé du modèle (UI).
- Multi-documents en source/exemple.
- Rendu Markdown amélioré (styles, titres, listes, tableaux).

### Étape 3 - Version avancée (>3 mois)

- Intégration d’une base vectorielle pour grands corpus.
- Gestion de projets utilisateurs.
- Authentification et stockage cloud.
- Dashboard de suivi et visualisation des exports.

---

## 7. Contraintes & Risques

- **Coûts :** utilisation d’API GPT (facturation au token).
- **Limites techniques :** taille maximale du prompt.
- **Risque utilisateur :** documents confidentiels → politiques de sécurité nécessaires.
- **Rendu Markdown :** risque de perte de mise en forme si export PDF/DOCX non correctement configuré.

---

## 8. Livrables

- Application Streamlit fonctionnelle avec rendu Markdown.
- Export PDF et DOCX.
- Documentation technique.
- Tests unitaires et scripts de déploiement.
- Cahier des charges mis à jour et détaillé par fichiers séparés pour modularité.

