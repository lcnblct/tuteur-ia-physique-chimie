import streamlit as st
import os
import re
# from groq import Groq
from dotenv import load_dotenv
import requests
from os import getenv

# Charger les variables d'environnement
load_dotenv()

# Guide de développement : voir DEVELOPMENT_GUIDE.md pour étendre l'application

st.set_page_config(
    page_title="Mon Assistant Physique-Chimie",
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

st.title("🧪 Mon Assistant Physique-Chimie")
st.markdown("**Ton assistant pour apprendre la physique et la chimie**")
st.markdown("---")

# Fonction pour charger le prompt spécialisé
def load_specialized_prompt(chapitre):
    """Charge le prompt spécialisé selon le chapitre sélectionné"""
    try:
        if chapitre == "Les trois états de la matière":
            prompt_path = "system_prompts/5e/organisation_et_transformations/trois_etats_matiere.md"
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        # Pour ajouter un nouveau prompt spécialisé, voir DEVELOPMENT_GUIDE.md
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
    model = getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")
    
    if not api_key:
        return "❌ **Clé API manquante**\n\nPour utiliser l'assistant, tu dois configurer ta clé API OpenRouter.\n\n1. Va sur https://openrouter.ai/\n2. Crée un compte et obtiens ta clé API\n3. Crée un fichier `.env` avec :\n```\nOPENROUTER_API_KEY=ta_cle_api_ici\n```\n\nDemande à ton professeur de t'aider !"
    
    if not base_url:
        return "❌ **URL de base manquante**\n\nLa configuration n'est pas complète. Contacte ton professeur !"
    
    try:
        # Préparer les messages avec le prompt système spécialisé
        full_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages
        
        # Debug: Afficher les détails de la requête (en mode développement)
        debug_mode = getenv("DEBUG_MODE", "false").lower() == "true"
        
        # Debug temporairement désactivé pour la production
        debug_mode = False
        
        if debug_mode:
            st.write(f"🔍 **Debug** : Modèle utilisé = {model}")
            st.write(f"🔍 **Debug** : URL = {base_url}/chat/completions")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": app_url or "http://localhost:8501",
                "X-Title": app_title or "Mon Assistant Physique-Chimie",
            },
            json={
                "model": model,
                "messages": full_messages,
                "temperature": 0.7,
                "max_tokens": 1500,
            },
            timeout=60
        )
        
        if debug_mode:
            st.write(f"🔍 **Debug** : Status code = {response.status_code}")
            if response.status_code != 200:
                st.write(f"🔍 **Debug** : Response = {response.text}")
        
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
    except requests.exceptions.RequestException as e:
        if "401" in str(e):
            return "❌ **Clé API invalide**\n\nTa clé API OpenRouter n'est pas valide. Vérifie qu'elle est correcte dans le fichier `.env`."
        elif "403" in str(e):
            return "❌ **Accès refusé (403)**\n\nProblème d'autorisation avec OpenRouter. Vérifie :\n\n1. **Ta clé API** est-elle valide ?\n2. **Ton compte OpenRouter** a-t-il des crédits ?\n3. **Le modèle** `google/gemini-2.5-flash-lite` est-il disponible ?\n\nEssaie de vérifier ton compte sur https://openrouter.ai/"
        elif "429" in str(e):
            return "❌ **Limite d'utilisation atteinte**\n\nTu as dépassé la limite d'utilisation d'OpenRouter. Essaie plus tard !"
        elif "timeout" in str(e).lower():
            return "❌ **Délai d'attente dépassé**\n\nLa réponse prend trop de temps. Essaie de nouveau !"
        else:
            return f"❌ **Erreur de connexion**\n\nProblème avec l'API OpenRouter : {str(e)[:100]}...\n\nVérifie ta connexion internet et essaie de nouveau !"
    except Exception as e:
        return f"❌ **Erreur inattendue**\n\nUn problème s'est produit : {str(e)[:100]}...\n\nEssaie de nouveau ou contacte ton professeur !"

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
        if st.button(
            n,
            key=f"niveau_{n}",
            help=f"Niveau {n}" if n == "5e" else "Bientôt disponible ! Choisis 5ème pour commencer 😊",
            use_container_width=True,
            disabled=(n != "5e")
        ):
            st.session_state["niveau"] = n
            if "theme_5e" in st.session_state:
                del st.session_state["theme_5e"]
            if "chapitre_5e" in st.session_state:
                del st.session_state["chapitre_5e"]
            st.rerun()
elif st.session_state["niveau"] == "5e" and "theme_5e" not in st.session_state:
    st.markdown("### Choisis un thème :")
    for theme in themes_5e:
        if st.button(
            theme,
            key=f"theme_{theme}",
            use_container_width=True,
            help="Tu peux choisir ce thème !" if theme == "Organisation et transformations de la matière" else "Bientôt disponible ! Choisis 'Organisation et transformations de la matière' pour commencer 🚀",
            disabled=(theme != "Organisation et transformations de la matière")
        ):
            st.session_state["theme_5e"] = theme
            if "chapitre_5e" in st.session_state:
                del st.session_state["chapitre_5e"]
            st.rerun()
elif st.session_state["niveau"] == "5e" and "theme_5e" in st.session_state and "chapitre_5e" not in st.session_state:
    theme_choisi = st.session_state["theme_5e"]
    st.markdown(f"### Thème : {theme_choisi}")
    st.markdown("#### Choisis un chapitre :")
    for chapitre in chapitres_5e[theme_choisi]:
        if st.button(
            chapitre,
            key=f"chapitre_{chapitre}",
            use_container_width=True,
            help="Tu peux choisir ce chapitre !" if chapitre == "Les trois états de la matière" else "Bientôt disponible ! Choisis 'Les trois états de la matière' pour commencer 💪",
            disabled=(chapitre != "Les trois états de la matière")
        ):
            st.session_state["chapitre_5e"] = chapitre
            st.rerun()
elif st.session_state["niveau"] == "5e" and "theme_5e" in st.session_state and "chapitre_5e" in st.session_state:
    st.success(f"✅ Niveau : 5e | Thème : {st.session_state['theme_5e']} | Chapitre : {st.session_state['chapitre_5e']}")
    
    # Charger le prompt spécialisé selon le chapitre
    chapitre = st.session_state["chapitre_5e"]
    system_prompt = load_specialized_prompt(chapitre)
    
    # Initialiser l'historique des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        # Message d'accueil automatique
        welcome_message = f"""🎯 **Salut ! Je suis ravi de t'aider !**

✅ **On va travailler sur :**
- **Niveau :** 5ème
- **Thème :** {st.session_state['theme_5e']}
- **Chapitre :** {st.session_state['chapitre_5e']}

🧪 **Je suis ton assistant pour apprendre** ce chapitre. Je vais te poser des questions pour t'aider à réfléchir et comprendre par toi-même.

💡 **Comment ça marche :**
- Pose tes questions sur le chapitre
- Je te guiderai avec des questions pour t'aider à réfléchir
- Tu vas construire tes connaissances toi-même

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
            with st.spinner("🤔 Je réfléchis..."):
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
    if st.button("🗑️ Recommencer", type="secondary"):
        st.session_state.messages = []
        st.rerun()
else:
    st.info(f"Tu as choisi le niveau : {st.session_state['niveau']}. Les thèmes spécifiques seront bientôt disponibles pour ce niveau.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🧪 Mon Assistant Physique-Chimie</p>
</div>
""", unsafe_allow_html=True)