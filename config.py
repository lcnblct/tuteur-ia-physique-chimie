"""
Configuration pour le Assistant Physique-Chimie
"""

# Configuration du modèle
MODEL_NAME = "moonshotai/kimi-k2-instruct"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1500

# Configuration de l'interface
PAGE_TITLE = "Mon Assistant Physique-Chimie"
PAGE_ICON = "🧪"

# Classes disponibles
CLASSES = {
    "6e (Cycle 3)": {
        "cycle": "Cycle 3",
        "description": "Observation macroscopique, expériences simples, vocabulaire simple",
        "themes": [
            "États et constitution de la matière à l'échelle macroscopique",
            "Différents types de mouvement",
            "Ressources en énergie et conversions d'énergie",
            "Signal et information"
        ]
    },
    "5e (Cycle 4)": {
        "cycle": "Cycle 4",
        "description": "Introduction progressive des modèles, distinction transformations physiques/chimiques",
        "themes": [
            "Organisation et transformations de la matière",
            "Mouvements et interactions",
            "L'énergie, ses transferts et ses conversions",
            "Des signaux pour observer et communiquer"
        ]
    },
    "4e (Cycle 4)": {
        "cycle": "Cycle 4",
        "description": "Approfondissement des modèles, lois de l'électricité quantitative",
        "themes": [
            "Organisation et transformations de la matière",
            "Mouvements et interactions",
            "L'énergie, ses transferts et ses conversions",
            "Des signaux pour observer et communiquer"
        ]
    },
    "3e (Cycle 4)": {
        "cycle": "Cycle 4",
        "description": "Consolidation des modèles, notions abstraites, formules d'énergie",
        "themes": [
            "Organisation et transformations de la matière",
            "Mouvements et interactions",
            "L'énergie, ses transferts et ses conversions",
            "Des signaux pour observer et communiquer"
        ]
    }
}

# Messages d'interface
WELCOME_MESSAGE = """
👋 **Bienvenue !** 

Je suis ton assistant spécialisé en physique-chimie. Je vais t'aider à comprendre les concepts en te posant des questions plutôt qu'en te donnant directement les réponses.

**Comment ça marche :**
- Je vais te poser des questions pour te faire réfléchir
- Tu vas construire ta compréhension étape par étape
- Je m'adapterai à ton niveau de classe
- On restera concentrés sur la physique-chimie ! 🎯

Commence par remplir tes informations dans la sidebar pour que je puisse t'aider au mieux.
"""

# Messages d'erreur
ERROR_MESSAGES = {
    "no_api_key": "❌ Clé API Groq manquante. Veuillez définir la variable d'environnement GROQ_API_KEY",
    "client_error": "❌ Erreur lors de l'initialisation du client Groq: {error}",
    "generation_error": "❌ Erreur lors de la génération de la réponse: {error}",
    "prompt_not_found": "⚠️ Fichier system_prompt.md non trouvé, utilisation du prompt par défaut"
}

# Styles CSS personnalisés
CUSTOM_CSS = """
<style>
.stApp {
    background-color: #f8f9fa;
}

.sidebar .sidebar-content {
    background-color: #ffffff;
}

.chat-message {
    border-radius: 15px;
    margin: 10px 0;
    padding: 15px;
}

.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
}

.assistant-message {
    background-color: #f3e5f5;
    border-left: 4px solid #9c27b0;
}

.info-box {
    background-color: #e8f5e8;
    border: 1px solid #4caf50;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}

.warning-box {
    background-color: #fff3e0;
    border: 1px solid #ff9800;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}
</style>
""" 