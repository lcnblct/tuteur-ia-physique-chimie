import streamlit as st
import os
import re
# from groq import Groq
from dotenv import load_dotenv
import requests
from os import getenv

# Charger les variables d'environnement
load_dotenv()

st.set_page_config(
    page_title="Tuteur IA Physique-Chimie",
    page_icon="🧪",
    layout="centered"
)

st.markdown("""
    <style>
    .big-button button {
        width: 100%;
        height: 3em;
        font-size: 1.3em;
        margin-bottom: 1em;
        border-radius: 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 Tuteur IA Physique-Chimie")
st.markdown("**Ton assistant pédagogique en physique-chimie**")
st.markdown("---")

# Fonction pour charger le prompt spécialisé
def load_specialized_prompt(chapitre):
    """Charge le prompt spécialisé selon le chapitre sélectionné"""
    try:
        if chapitre == "Les trois états de la matière":
            prompt_path = "system_prompts/5e/organisation_et_transformations/trois_etats_matiere.md"
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            # Pour les autres chapitres, utiliser le prompt général
            with open("system_prompt.md", "r", encoding="utf-8") as f:
                return f.read()
    except FileNotFoundError:
        return """Vous êtes un tuteur IA expert en physique-chimie pour les cycles 3 et 4 du système éducatif français. 
        Votre mission est de guider l'élève étape par étape pour qu'il construise lui-même sa compréhension. 
        Utilisez la méthode socratique : posez des questions pour guider la réflexion plutôt que de donner les réponses."""

# Fonction pour générer une réponse avec le prompt spécialisé
def generate_response_with_specialized_prompt(messages, system_prompt):
    """Génère une réponse avec OpenRouter via l'API REST avec un prompt spécialisé"""
    api_key = getenv("OPENROUTER_API_KEY")
    base_url = getenv("OPENROUTER_BASE_URL")
    app_url = getenv("APP_URL")
    app_title = getenv("APP_TITLE")
    
    if not api_key or not base_url:
        return "❌ Clé API OpenRouter ou URL manquante. Vérifiez le fichier .env"
    
    try:
        # Préparer les messages avec le prompt système spécialisé
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
        content = re.sub(r'◁think▷.*?◁/think▷', '', content, flags=re.DOTALL)
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        content = re.sub(r'<thinking>.*?</thinking>', '', content, flags=re.DOTALL)
        
        # Nettoyer les espaces multiples
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = content.strip()
        
        return content
    except Exception as e:
        return f"❌ Erreur OpenRouter: {str(e)}"

# Dictionnaire des chapitres de 5e par thème
chapitres_5e = {
    "Organisation et transformations de la matière": [
        "Les trois états de la matière",
        "Les changements d'état",
        "Mesures de masse et de volume",
        "Mélanges de liquides et de solides",
        "Identification d'une espèce chimique"
    ],
    "Mouvement et interactions": [
        "Mouvement d'un objet"
    ],
    "L'énergie, ses transferts et ses conversions": [
        "Les différentes formes d'énergie"
    ],
    "Des signaux pour observer et communiquer": [
        "Matériaux conducteurs et isolants. Sécurité électrique",
        "Circuits électriques en série et en dérivation",
        "Signaux sonores",
        "Signaux lumineux"
    ]
}

themes_5e = list(chapitres_5e.keys())

# Wizard étape par étape
if "niveau" not in st.session_state:
    st.markdown("### Choisis ton niveau :")
    for n in ["6e", "5e", "4e", "3e"]:
        if st.button(n, key=f"niveau_{n}", help=f"Niveau {n}", use_container_width=True):
            st.session_state["niveau"] = n
            # Reset étapes suivantes
            if "theme_5e" in st.session_state:
                del st.session_state["theme_5e"]
            if "chapitre_5e" in st.session_state:
                del st.session_state["chapitre_5e"]
            st.experimental_rerun()
elif st.session_state["niveau"] == "5e" and "theme_5e" not in st.session_state:
    st.markdown("### Choisis un thème :")
    for theme in themes_5e:
        if st.button(theme, key=f"theme_{theme}", use_container_width=True):
            st.session_state["theme_5e"] = theme
            if "chapitre_5e" in st.session_state:
                del st.session_state["chapitre_5e"]
            st.experimental_rerun()
elif st.session_state["niveau"] == "5e" and "theme_5e" in st.session_state and "chapitre_5e" not in st.session_state:
    theme_choisi = st.session_state["theme_5e"]
    st.markdown(f"### Thème : {theme_choisi}")
    st.markdown("#### Choisis un chapitre :")
    for chapitre in chapitres_5e[theme_choisi]:
        if st.button(chapitre, key=f"chapitre_{chapitre}", use_container_width=True):
            st.session_state["chapitre_5e"] = chapitre
            st.experimental_rerun()
elif st.session_state["niveau"] == "5e" and "theme_5e" in st.session_state and "chapitre_5e" in st.session_state:
    st.success(f"Niveau : 5e | Thème : {st.session_state['theme_5e']} | Chapitre : {st.session_state['chapitre_5e']}")
    
    # Charger le prompt spécialisé selon le chapitre
    chapitre = st.session_state["chapitre_5e"]
    system_prompt = load_specialized_prompt(chapitre)
    
    # Initialiser l'historique des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        # Message d'accueil automatique
        welcome_message = f"""🎯 **Bienvenue dans ton espace d'apprentissage !**

✅ **Tu es ici :**
- **Niveau :** 5ème
- **Thème :** {st.session_state['theme_5e']}
- **Chapitre :** {st.session_state['chapitre_5e']}

🧪 **Je suis ton tuteur IA spécialisé** pour ce chapitre. Je vais t'accompagner avec la méthode socratique : je te poserai des questions pour te faire réfléchir et construire ta compréhension étape par étape.

💡 **Comment ça marche :**
- Pose tes questions sur le chapitre
- Je te guiderai avec des questions pour t'aider à réfléchir
- Tu construiras toi-même tes connaissances

**Prêt(e) à commencer ? Pose ta première question !** 🚀"""
        
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    
    # Afficher l'historique
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Zone de saisie
    if prompt := st.chat_input("Pose ta question sur ce chapitre..."):
        # Ajouter le message élève
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
                
                # Générer la réponse avec le prompt spécialisé
                response = generate_response_with_specialized_prompt(messages_for_api, system_prompt)
                
                # Afficher la réponse
                st.markdown(response)
                
                # Ajouter la réponse à l'historique
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Bouton pour effacer l'historique
    if st.button("🗑️ Effacer l'historique", type="secondary"):
        st.session_state.messages = []
        st.rerun()
else:
    st.info(f"Tu as choisi le niveau : {st.session_state['niveau']}. Les thèmes spécifiques seront bientôt disponibles pour ce niveau.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🧪 Tuteur IA Physique-Chimie propulsé par <a href='https://openrouter.ai' target='_blank'>OpenRouter</a> et <a href='https://streamlit.io' target='_blank'>Streamlit</a></p>
</div>
""", unsafe_allow_html=True)