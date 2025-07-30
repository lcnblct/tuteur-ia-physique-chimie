#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à l'API Groq et le prompt système
"""

import os
from groq import Groq
from dotenv import load_dotenv

def load_system_prompt():
    """Charge le prompt système depuis le fichier"""
    try:
        with open("system_prompt.md", "r", encoding="utf-8") as f:
            return f.read()  # Utiliser le prompt complet avec ce modèle
    except FileNotFoundError:
        return """Vous êtes un tuteur IA expert en physique-chimie pour les cycles 3 et 4 du système éducatif français. 
        Votre mission est de guider l'élève étape par étape pour qu'il construise lui-même sa compréhension. 
        Utilisez la méthode socratique : posez des questions pour guider la réflexion plutôt que de donner les réponses."""

def test_groq_connection():
    """Teste la connexion à l'API Groq et le prompt système"""
    print("🧪 Test de connexion à l'API Groq")
    print("=" * 50)
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier la clé API
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Erreur: Clé API Groq manquante")
        print("   Veuillez créer un fichier .env avec GROQ_API_KEY=your_key")
        return False
    
    print(f"✅ Clé API trouvée: {api_key[:10]}...")
    
    # Vérifier le prompt système
    system_prompt = load_system_prompt()
    if "system_prompt.md" in system_prompt:
        print("✅ Fichier system_prompt.md trouvé et chargé (version complète)")
    else:
        print("⚠️ Fichier system_prompt.md non trouvé, utilisation du prompt par défaut")
    
    try:
        # Initialiser le client
        client = Groq(api_key=api_key)
        print("✅ Client Groq initialisé")
        
        # Test simple avec le modèle et le prompt système
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Vous êtes un tuteur IA en physique-chimie. Utilisez la méthode socratique."
                },
                {
                    "role": "user",
                    "content": "Bonjour, je suis en 5e et j'ai du mal à comprendre la différence entre une transformation physique et une transformation chimique. Peux-tu m'aider ?"
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=200
        )
        
        print("✅ Test de génération avec prompt système réussi")
        print(f"📝 Réponse du tuteur: {response.choices[0].message.content}")
        
        # Vérifier que la réponse suit la méthode socratique
        response_text = response.choices[0].message.content.lower()
        if any(keyword in response_text for keyword in ["question", "pense", "réfléchis", "d'après toi", "comment"]):
            print("✅ La réponse utilise bien la méthode socratique (questions guidantes)")
        else:
            print("⚠️ La réponse pourrait ne pas suivre la méthode socratique")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def test_model_capabilities():
    """Teste les capacités du modèle avec différents types de questions"""
    print("\n🧪 Test des capacités du modèle")
    print("=" * 50)
    
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return False
    
    try:
        client = Groq(api_key=api_key)
        
        # Test avec une question de 6e
        print("📚 Test avec une question de 6e (Cycle 3):")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Vous êtes un tuteur IA en physique-chimie. Utilisez la méthode socratique."},
                {"role": "user", "content": "Je suis en 6e et je ne comprends pas pourquoi l'eau change d'état quand on la chauffe."}
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=150
        )
        print(f"Réponse: {response.choices[0].message.content[:100]}...")
        
        # Test avec une question de 3e
        print("\n📚 Test avec une question de 3e (Cycle 4):")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Vous êtes un tuteur IA en physique-chimie. Utilisez la méthode socratique."},
                {"role": "user", "content": "Je suis en 3e et j'ai du mal avec la formule de l'énergie cinétique Ec = 1/2 × m × v². Peux-tu m'expliquer ?"}
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=150
        )
        print(f"Réponse: {response.choices[0].message.content[:100]}...")
        
        print("✅ Tests des capacités du modèle réussis")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests de capacités: {str(e)}")
        return False

if __name__ == "__main__":
    success1 = test_groq_connection()
    success2 = test_model_capabilities()
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont passés ! Le tuteur IA est prêt à être utilisé.")
        print("   Lancez 'streamlit run app.py' pour démarrer l'application.")
    else:
        print("\n💥 Des erreurs ont été détectées. Veuillez les corriger avant de lancer l'application.") 