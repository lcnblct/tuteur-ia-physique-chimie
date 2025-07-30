# 🧪 Mon Assistant Physique-Chimie

Un assistant IA spécialisé pour aider les élèves à apprendre la physique et la chimie en utilisant la méthode socratique.

## 🚀 Installation et Configuration

### 1. Prérequis
- Python 3.8 ou plus récent
- Une clé API OpenRouter (gratuite)

### 2. Installation
```bash
# Cloner le projet
git clone <url-du-repo>
cd chatbot

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration
1. **Obtenir une clé API OpenRouter** :
   - Va sur [https://openrouter.ai/](https://openrouter.ai/)
   - Crée un compte gratuit
   - Va dans "API Keys"
   - Crée une nouvelle clé API

2. **Configurer les variables d'environnement** :
   ```bash
   # Copier le fichier d'exemple
   cp env_example.txt .env
   
   # Éditer le fichier .env et remplacer par ta vraie clé API
   nano .env
   ```

3. **Vérifier la configuration** :
   ```bash
   python setup.py
   ```

### 4. Lancer l'application
```bash
streamlit run app.py
```

## 🎯 Fonctionnalités

- **Interface intuitive** : Navigation par niveau et thème
- **Prompts spécialisés** : Adaptés à chaque chapitre
- **Méthode socratique** : L'IA pose des questions pour guider l'apprentissage
- **Historique des conversations** : Suivi des échanges
- **Gestion d'erreurs améliorée** : Messages d'erreur clairs et utiles

## 📚 Chapitres disponibles

### 5ème (Cycle 4)
- **Organisation et transformations de la matière**
  - Les trois états de la matière ✅
  - Les changements d'état (bientôt)
  - Mesures de masse et de volume (bientôt)
  - Mélanges de liquides et de solides (bientôt)
  - Identification d'une espèce chimique (bientôt)

*Autres thèmes et niveaux en développement*

## 🔧 Développement

Voir `DEVELOPMENT_GUIDE.md` pour étendre l'application.

## 🐛 Dépannage

### Erreur "Clé API manquante"
- Vérifie que le fichier `.env` existe
- Vérifie que `OPENROUTER_API_KEY` est défini
- Vérifie que la clé API est valide

### Erreur "Limite d'utilisation atteinte"
- OpenRouter a une limite gratuite
- Attends quelques minutes ou upgrade ton compte

### Erreur "Délai d'attente dépassé"
- Problème de connexion internet
- Essaie de nouveau

## 📝 Structure du projet

```
chatbot/
├── app.py                 # Application principale
├── setup.py              # Script de configuration
├── config.py             # Configuration
├── requirements.txt      # Dépendances
├── env_example.txt      # Exemple de variables d'environnement
├── system_prompt.md     # Prompt système général
├── system_prompts/      # Prompts spécialisés par chapitre
└── README.md           # Ce fichier
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir `DEVELOPMENT_GUIDE.md` pour les détails. 