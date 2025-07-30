# Guide de Développement - Assistant Physique-Chimie

## Comment étendre l'application avec de nouveaux niveaux, thèmes et chapitres

### 1. Activer un nouveau niveau (6e, 4e, 3e)

**Localisation :** Ligne ~130 dans `app.py`
**Action :** Modifier la condition `disabled=(n != "5e")`

**Exemple pour activer 6e :**
```python
# Remplacer :
disabled=(n != "5e")

# Par :
disabled=(n not in ["5e", "6e"])
```

**Pour activer plusieurs niveaux :**
```python
disabled=(n not in ["5e", "6e", "4e"])
```

### 2. Activer un nouveau thème

**Localisation :** Ligne ~145 dans `app.py`
**Action :** Modifier la condition `disabled=(theme != "Organisation et transformations de la matière")`

**Exemple pour activer "Mouvement et interactions" :**
```python
# Remplacer :
disabled=(theme != "Organisation et transformations de la matière")

# Par :
disabled=(theme not in ["Organisation et transformations de la matière", "Mouvement et interactions"])
```

### 3. Activer un nouveau chapitre

**Localisation :** Ligne ~160 dans `app.py`
**Action :** Modifier la condition `disabled=(chapitre != "Les trois états de la matière")`

**Exemple pour activer "Les changements d'état" :**
```python
# Remplacer :
disabled=(chapitre != "Les trois états de la matière")

# Par :
disabled=(chapitre not in ["Les trois états de la matière", "Les changements d'état"])
```

### 4. Créer un prompt spécialisé

#### Étape 1 : Créer le fichier prompt
**Chemin :** `system_prompts/5e/organisation_et_transformations/NOM_CHAPITRE.md`

**Exemple :** `system_prompts/5e/organisation_et_transformations/changements_etat.md`

#### Étape 2 : Ajouter la condition dans load_specialized_prompt()
**Localisation :** Après ligne ~40 dans `app.py`

**Ajouter cette condition :**
```python
elif chapitre == "NOM_CHAPITRE":
    prompt_path = "system_prompts/5e/organisation_et_transformations/NOM_CHAPITRE.md"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
```

**Exemple concret pour "Les changements d'état" :**
```python
elif chapitre == "Les changements d'état":
    prompt_path = "system_prompts/5e/organisation_et_transformations/changements_etat.md"
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()
```

### 5. Workflow complet pour un nouveau chapitre

**Exemple :** Ajouter "Les changements d'état"

1. **Créer le fichier prompt :**
   ```
   system_prompts/5e/organisation_et_transformations/changements_etat.md
   ```

2. **Modifier app.py ligne ~160 :**
   ```python
   disabled=(chapitre not in ["Les trois états de la matière", "Les changements d'état"])
   ```

3. **Ajouter dans load_specialized_prompt() :**
   ```python
   elif chapitre == "Les changements d'état":
       prompt_path = "system_prompts/5e/organisation_et_transformations/changements_etat.md"
       with open(prompt_path, "r", encoding="utf-8") as f:
           return f.read()
   ```

4. **Tester :**
   - Lancer l'application
   - Vérifier que le bouton est actif
   - Tester le chat avec le nouveau prompt

### 6. Structure des dossiers

```
system_prompts/
├── 5e/
│   ├── organisation_et_transformations/
│   │   ├── trois_etats_matiere.md ✅
│   │   ├── changements_etat.md (à créer)
│   │   └── ...
│   ├── mouvement_et_interactions/
│   │   └── ...
│   └── ...
├── 6e/
│   └── ...
└── ...
```

### 7. Notes importantes

- **Noms de fichiers :** Doivent correspondre exactement aux noms des chapitres
- **Encodage :** Toujours utiliser `encoding="utf-8"`
- **Structure :** Respecter la hiérarchie niveau/thème/chapitre
- **Test :** Toujours tester après modification

### 8. Exemples de prompts existants

- **Prompt spécialisé :** `trois_etats_matiere.md` (190 lignes, ultra-spécialisé)
- **Prompt général :** `system_prompt.md` (517 lignes, générique)

### 9. Troubleshooting

**Problème :** Le bouton reste grisé
**Solution :** Vérifier que la condition `disabled=` a bien été modifiée

**Problème :** Erreur "File not found"
**Solution :** Vérifier le chemin du fichier prompt et l'encodage

**Problème :** Le prompt ne se charge pas
**Solution :** Vérifier que la condition dans `load_specialized_prompt()` correspond exactement au nom du chapitre 