import streamlit as st
import os
# from groq import Groq
from dotenv import load_dotenv
import requests
from os import getenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Tuteur IA Physique-Chimie",
    page_icon="🧪",
    layout="centered"
)

# Titre de l'application
st.title("🧪 Tuteur IA Physique-Chimie")
st.markdown("**Votre assistant pédagogique spécialisé en physique-chimie (Cycles 3 & 4)**")
st.markdown("---")

# Initialisation du client Groq
# def init_groq_client():
#     """Initialise le client Groq avec la clé API"""
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         st.error("❌ Clé API Groq manquante. Veuillez définir la variable d'environnement GROQ_API_KEY")
#         return None
#     try:
#         client = Groq(api_key=api_key)
#         return client
#     except Exception as e:
#         st.error(f"❌ Erreur lors de l'initialisation du client Groq: {str(e)}")
#         return None
# client = init_groq_client()

# Configuration du modèle - Changement pour un modèle avec beaucoup plus de tokens
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"  # Limite de 30000 TPM

# Initialisation de l'historique des conversations
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fonction pour charger le prompt système complet
def load_system_prompt():
    """Charge le prompt système complet depuis le fichier"""
    try:
        with open("system_prompt.md", "r", encoding="utf-8") as f:
            return f.read()  # Utiliser le prompt complet avec ce modèle
    except FileNotFoundError:
        return """Vous êtes un tuteur IA expert en physique-chimie pour les cycles 3 et 4 du système éducatif français. 
        Votre mission est de guider l'élève étape par étape pour qu'il construise lui-même sa compréhension. 
        Utilisez la méthode socratique : posez des questions pour guider la réflexion plutôt que de donner les réponses.
        
        Règles importantes :
        - Posez des questions pour faire réfléchir l'élève
        - Ne donnez jamais les réponses directement
        - Adaptez le niveau selon la classe mentionnée
        - Restez uniquement sur la physique-chimie
        - Utilisez un ton bienveillant et encourageant"""

# Fonction pour générer une réponse avec le prompt système
def generate_response(messages):
    """Génère une réponse avec OpenRouter via l'API REST"""
    api_key = getenv("OPENROUTER_API_KEY")
    base_url = getenv("OPENROUTER_BASE_URL")
    app_url = getenv("APP_URL")
    app_title = getenv("APP_TITLE")
    
    if not api_key or not base_url:
        return "❌ Clé API OpenRouter ou URL manquante. Vérifiez le fichier .env"
    
    try:
        # Charger le prompt système complet
        system_prompt = load_system_prompt()
        
        # Préparer les messages avec le prompt système
        full_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": app_url,
                "X-Title": app_title,
            },
            json={
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "messages": full_messages,
                "temperature": 0.7,
                "max_tokens": 1500,
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Nettoyer les balises de réflexion
        import re
        content = re.sub(r'◁think▷.*?◁/think▷', '', content, flags=re.DOTALL)
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        content = re.sub(r'<thinking>.*?</thinking>', '', content, flags=re.DOTALL)
        
        # Nettoyer les espaces multiples
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = content.strip()
        
        return content
    except Exception as e:
        return f"❌ Erreur OpenRouter: {str(e)}"

# Affichage principal
st.markdown("""
### 🎯 Mon rôle
- **Tuteur IA spécialisé** en physique-chimie (cycles 3 & 4)
- **Méthode socratique** : je te pose des questions pour te faire réfléchir
- **Pas de réponses directes** : je t'aide à construire ta compréhension
- **Adaptation au niveau** : contenu adapté selon ta classe
- **Focus exclusif** : uniquement sur la physique-chimie

### 📚 Programmes couverts
**Cycle 3 (6e)** : États de la matière, mouvements, énergie, signaux  
**Cycle 4 (5e, 4e, 3e)** : Transformations de la matière, interactions, conversions d'énergie, signaux
""")

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie pour l'élève
if prompt := st.chat_input("Pose ta question ou décris ton problème..."):
    # Ajouter le message élève à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Afficher le message élève
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Afficher le message tuteur avec un spinner
    with st.chat_message("assistant"):
        with st.spinner("🤔 Je réfléchis à ta question..."):
            # Préparer les messages pour l'API
            messages_for_api = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in st.session_state.messages
            ]
            
            # Générer la réponse
            response = generate_response(messages_for_api)
            
            # Afficher la réponse
            st.markdown(response)
            
            # Ajouter la réponse à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})

# Bouton pour effacer l'historique
if st.button("🗑️ Effacer l'historique", type="secondary"):
    st.session_state.messages = []
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🧪 Tuteur IA Physique-Chimie propulsé par <a href='https://openrouter.ai' target='_blank'>OpenRouter</a> et <a href='https://streamlit.io' target='_blank'>Streamlit</a></p>
    <p>Modèle: mistralai/mistral-small-3.2-24b-instruct:free | Méthode Socratique</p>
</div>
""", unsafe_allow_html=True) 