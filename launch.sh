#!/bin/bash

# Script de lancement pour le Assistant Physique-Chimie

echo "🧪 Lancement du Assistant Physique-Chimie"
echo "=========================================="

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
echo "📚 Vérification des dépendances..."
pip install -r requirements.txt > /dev/null 2>&1

# Vérifier la configuration
echo "🔍 Vérification de la configuration..."
if [ ! -f ".env" ]; then
    echo "❌ Fichier .env manquant !"
    echo "   Créez le fichier .env avec votre clé API Groq :"
    echo "   GROQ_API_KEY=votre_cle_api_ici"
    exit 1
fi

# Lancer l'application
echo "🚀 Lancement de l'application..."
echo "   L'application sera accessible sur : http://localhost:8501"
echo "   Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

streamlit run app.py 