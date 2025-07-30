# 🧪 Tuteur IA Physique-Chimie

**Votre assistant pédagogique spécialisé en physique-chimie (Cycles 3 & 4)**

## 🎯 Rôle du Tuteur IA

- **Tuteur IA spécialisé** en physique-chimie (cycles 3 & 4)
- **Méthode socratique** : pose des questions pour faire réfléchir
- **Pas de réponses directes** : aide à construire la compréhension
- **Adaptation au niveau** : contenu adapté selon la classe
- **Focus exclusif** : uniquement sur la physique-chimie

## 📚 Programmes couverts

**Cycle 3 (6e)** : États de la matière, mouvements, énergie, signaux  
**Cycle 4 (5e, 4e, 3e)** : Transformations de la matière, interactions, conversions d'énergie, signaux

## 🚀 Déploiement

### Option 1 : Streamlit Cloud (Recommandé - Gratuit)

1. **Créez un compte** sur [share.streamlit.io](https://share.streamlit.io)
2. **Connectez votre GitHub** et sélectionnez ce repository
3. **Configurez les variables d'environnement** :
   - `GROQ_API_KEY` = votre clé API Groq
4. **Déployez** ! L'app sera accessible via une URL publique

### Option 2 : Heroku

1. **Installez Heroku CLI**
2. **Déployez** :
   ```bash
   heroku create votre-app-name
   heroku config:set GROQ_API_KEY=votre_cle_api
   git push heroku main
   ```

## 🔧 Installation locale

```bash
# Cloner le repository
git clone <votre-repo>
cd chatbot

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env avec votre clé API
echo "GROQ_API_KEY=votre_cle_api_groq" > .env

# Lancer l'application
streamlit run app.py
```

## 📁 Structure du projet

```
chatbot/
├── app.py                 # Application principale Streamlit
├── system_prompt.md       # Prompt système complet
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement (clé API)
├── test_groq.py          # Script de test de l'API
├── config.py             # Configuration centralisée
├── launch.sh             # Script de lancement
├── Procfile              # Configuration Heroku
└── README.md             # Documentation
```

## 🔑 Configuration de l'API Groq

1. **Obtenez votre clé API** sur [console.groq.com](https://console.groq.com)
2. **Créez le fichier `.env`** :
   ```
   GROQ_API_KEY=gsk_votre_cle_api_ici
   ```

## 🧪 Test de l'application

```bash
# Tester la connexion API
python test_groq.py

# Lancer l'application
streamlit run app.py
```

## 📊 Modèle utilisé

- **Modèle** : `meta-llama/llama-4-scout-17b-16e-instruct`
- **Limite** : 30 000 TPM (Tokens Per Minute)
- **Méthode** : Socratique (questions guidantes)

## 🎨 Personnalisation

- **Thème** : Modifiable dans `.streamlit/config.toml`
- **Prompt système** : Éditable dans `system_prompt.md`
- **Configuration** : Centralisée dans `config.py`

---

**Propulsé par** [Groq](https://groq.com) et [Streamlit](https://streamlit.io) 🚀 