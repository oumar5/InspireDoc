# InspireDoc

## 1. Description du projet

InspireDoc est une application web développée avec Streamlit permettant de générer automatiquement des documents au format Markdown à partir de documents sources et d'exemples fournis par l'utilisateur. Le document généré peut être exporté en PDF ou DOCX et est rendu de manière lisible et designée directement dans l'application.

L'objectif est d'aider les utilisateurs à créer rapidement des documents cohérents, professionnels et respectant un style donné.

---

## 2. Fonctionnalités principales

1. **Upload de documents**

   - Formats supportés : PDF, TXT, DOCX
   - Trois types de documents :
     - Documents sources : contenu à utiliser
     - Documents exemples : style et structure à suivre
     - Nouveau document : demande spécifique de génération

2. **Extraction et nettoyage**

   - Extraction automatique du texte brut depuis les fichiers
   - Nettoyage et normalisation (suppression de caractères spéciaux, espaces multiples, etc.)

3. **Génération via LLM**

   - Construction de prompts structurés pour GPT-4 ou équivalent
   - Génération de documents Markdown respectant le style des exemples et le contenu des sources

4. **Affichage et export**

   - Affichage du Markdown généré directement dans Streamlit
   - Export possible en PDF ou DOCX en conservant la mise en forme

5. **Architecture modulaire**

   - Séparation de la logique métier (`core/`) et de l'interface (`pages/`)
   - Gestion des fichiers séparés pour ingestion, nettoyage, génération et rendu

---

## 3. Structure des dossiers

```
inspiredoc/
├── app.py
├── config/
│   └── settings.py
├── data/
│   ├── uploads/
│   ├── processed/
│   └── exports/
├── core/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── llm/
│   ├── rendering/
│   ├── services/
│   └── utils/
├── pages/
│   ├── home.py
│   ├── generation.py
│   ├── settings.py
│   └── about.py
├── tests/
│   └── ...
└── README.md
```

---

## 4. Installation

1. Cloner le dépôt :

```bash
https://github.com/oumar5/InspireDoc.git
cd inspiredoc
```

2. Créer un environnement virtuel et installer les dépendances :

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Configurer les clés API dans `config/settings.py` si nécessaire.

---

## 5. Lancement de l'application

```bash
streamlit run app.py
```

- La page d'accueil (`home`) permet de naviguer vers la génération de documents.
- Les pages additionnelles incluent `settings` et `about`.

---

## 6. Utilisation

1. Upload des documents sources et exemples.
2. Saisir la demande spécifique pour le nouveau document.
3. Cliquer sur "Générer".
4. Visualiser le document Markdown généré.
5. Exporter en PDF ou DOCX.

---

## 7. Tests

- Les tests unitaires se trouvent dans le dossier `tests/`.
- Pour lancer les tests :

```bash
pytest tests/
```

---

## 8. Contributions

- Forker le dépôt
- Créer une branche feature
- Soumettre une pull request

---

## 9. Licence

Indiquer la licence choisie pour le projet.

