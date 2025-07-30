#!/usr/bin/env python3
"""
Script de configuration pour l'Assistant Physique-Chimie
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Vérifie si le fichier .env existe et affiche les instructions"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Fichier .env trouvé !")
        return True
    else:
        print("❌ Fichier .env manquant")
        print("\n📝 Pour créer le fichier .env :")
        print("1. Copie le contenu de env_example.txt")
        print("2. Crée un fichier .env avec les mêmes variables")
        print("3. Remplace 'your_openrouter_api_key_here' par ta vraie clé API")
        print("\n🔑 Pour obtenir une clé API OpenRouter :")
        print("1. Va sur https://openrouter.ai/")
        print("2. Crée un compte gratuit")
        print("3. Va dans 'API Keys'")
        print("4. Crée une nouvelle clé API")
        return False

def check_required_vars():
    """Vérifie si les variables d'environnement requises sont définies"""
    required_vars = [
        "OPENROUTER_API_KEY",
        "OPENROUTER_BASE_URL",
        "APP_URL",
        "APP_TITLE"
    ]
    
    # Variables optionnelles avec valeurs par défaut
    optional_vars = {
        "OPENROUTER_MODEL": "google/gemini-2.5-flash-lite"
    }
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables manquantes : {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Toutes les variables d'environnement sont configurées !")
        
        # Afficher les variables optionnelles
        print("\n📋 Configuration actuelle :")
        for var, default_value in optional_vars.items():
            current_value = os.getenv(var, default_value)
            print(f"  {var}: {current_value}")
        
        return True

def main():
    print("🔧 Configuration de l'Assistant Physique-Chimie")
    print("=" * 50)
    
    # Charger les variables d'environnement depuis .env
    load_dotenv()
    
    # Vérifier le fichier .env
    env_exists = check_env_file()
    
    # Vérifier les variables d'environnement
    vars_ok = check_required_vars()
    
    print("\n" + "=" * 50)
    
    if env_exists and vars_ok:
        print("🎉 Configuration complète ! Tu peux lancer l'application avec :")
        print("streamlit run app.py")
    else:
        print("⚠️  Configuration incomplète. Suis les instructions ci-dessus.")
        print("\n💡 Une fois configuré, lance l'application avec :")
        print("streamlit run app.py")

if __name__ == "__main__":
    main() 