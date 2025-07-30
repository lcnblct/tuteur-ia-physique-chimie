#!/usr/bin/env python3
"""
Script de lancement pour l'application ChatBot Groq
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import streamlit
        # import groq
        import dotenv
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("   Installez les dépendances avec: pip install -r requirements.txt")
        return False

def check_env_file():
    """Vérifie que le fichier .env existe"""
    print("🔍 Vérification du fichier .env...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Fichier .env manquant")
        print("   Créez le fichier .env avec votre clé API Groq:")
        print("   GROQ_API_KEY=your_groq_api_key_here")
        return False
    
    # Vérifier que la clé API est définie
    load_dotenv()
    # api_key = os.getenv("GROQ_API_KEY")
    # if not api_key or api_key == "your_groq_api_key_here":
    #     print("❌ Clé API Groq non configurée dans .env")
    #     print("   Remplacez 'your_groq_api_key_here' par votre vraie clé API")
    #     return False
    
    print("✅ Fichier .env configuré")
    return True

def run_tests():
    """Lance les tests de connexion"""
    print("🧪 Lancement des tests de connexion...")
    
    try:
        result = subprocess.run([sys.executable, "test_groq.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tests de connexion réussis")
            return True
        else:
            print("❌ Tests de connexion échoués")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        return False

def launch_app():
    """Lance l'application Streamlit"""
    print("🚀 Lancement de l'application...")
    print("   L'application sera accessible sur: http://localhost:8501")
    print("   Appuyez sur Ctrl+C pour arrêter l'application")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def main():
    """Fonction principale"""
    print("🤖 ChatBot Groq - Script de lancement")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_requirements():
        return
    
    if not check_env_file():
        return
    
    if not run_tests():
        return
    
    # Lancement de l'application
    launch_app()

if __name__ == "__main__":
    # Import ici pour éviter les erreurs si dotenv n'est pas installé
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("❌ python-dotenv n'est pas installé")
        print("   Installez-le avec: pip install python-dotenv")
        sys.exit(1)
    
    main() 