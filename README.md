# Guide Simple - Transférer vos Pokémon entre versions Cobblemon

**Ce guide vous aide à transférer vos Pokémon du PC de Cobblemon Academy 2.0 vers Cobblemon 1.6**

---

## Ce dont vous avez besoin

1. **Python installé** sur votre ordinateur (voir instructions détaillées ci-dessous)
2. **Le script de conversion** (déjà dans ce dossier)

---

## Installation de Python (si nécessaire)

### Télécharger et installer Python

1. Téléchargez Python : [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Lancez l'installeur Python
3. **Important** : Cochez "Add Python to PATH" avant de continuer
4. L'installeur va ouvrir une invite de commande où vous devrez répondre par `Y` (Yes) ou `n` (No)

### Désactiver les alias Windows (Important!)

Windows possède des alias qui peuvent bloquer Python. Il faut les désactiver :

1. Ouvrez **Paramètres Windows**
2. Allez dans **Applications** → **Applications et fonctionnalités**
3. Cliquez sur **Alias d'exécution d'applications**
4. **Désactivez** ces deux éléments :
   - `python.exe`
   - `python3.exe`

### Vérifier l'installation

Ouvrez **PowerShell** et tapez :
```powershell
python --version
pip --version
```

### Si pip n'est pas reconnu

####  Vérifier si pip existe :
```powershell
python -m pip --version
```

#### 2. Forcer la création de pip.exe :
```powershell
python -m pip install --upgrade --force-reinstall pip
python -m pip install --upgrade setuptools wheel
```

#### 3. Vérifier la présence des fichiers pip :
```powershell
dir C:\Users\VOTRE_NOM\AppData\Local\Python\pythoncore-3.14-64\Scripts
```

Vous devez voir :
- `pip.exe`
- `pip3.exe`
- `pip3.14.exe`

**Note** : Remplacez `VOTRE_NOM` par votre nom d'utilisateur Windows, et `3.14` par votre version de Python.

#### 4. Ajouter pip au PATH Windows :

 Tapez **"Modifier les variables d'environnement système"** dans la recherche Windows
2. Cliquez sur **Variables d'environnement**
3. Dans **Variables utilisateur**, sélectionnez **Path** et cliquez sur **Modifier**
4. Cliquez sur **Nouveau** et ajoutez ces deux chemins (adaptez avec votre nom d'utilisateur et version Python) :
   ```
   C:\Users\VOTRE_NOM\AppData\Local\Python\pythoncore-3.14-64\
   C:\Users\VOTRE_NOM\AppData\Local\Python\pythoncore-3.14-64\Scripts
   ```
5. Cliquez sur **OK** partout pour fermer
6. **Fermez et rouvrez PowerShell** pour appliquer les changements

### Test final et installation de la bibliothèque nécessaire

Dans PowerShell :
```powershell
pip --version
pip install nbtlib
```

---

## Étapes de Conversion

### Étape 1 : Trouver les chemins de vos mondes

#### Pour trouver le chemin de votre ANCIEN monde :

 Ouvrez le **Launcher CurseForge**
2. Faites un **clic droit** sur "Cobblemon Academy 2.0 ou Cacademy"
3. Cliquez sur "**Ouvrir le dossier**"
4. Double-cliquez sur : `saves` → puis votre monde
5. Dans la barre d'adresse en haut, cliquez et **copiez** le chemin complet

**Exemple de chemin** :
```
C:\Users\VotreNom\curseforge\minecraft\Instances\Cobblemon Academy 2.0\saves\Nouveau monde
```

#### Pour trouver le chemin de votre NOUVEAU monde:

Faites la même chose mais pour votre nouveau modpack ex: "CacademyV2"

**Exemple de chemin** :
```
C:\Users\VotreNom\curseforge\minecraft\Instances\Cacademy v2\saves\world-DEMO
```

### Étape 3 : Lancer la conversion

 Ouvrez un **PowerShell**, à l'emplacement du script :

2. Dans votre invite de commande, lancez le script :
   ```
   python convert_pokemon_gui.py
   ```

3. Le script va :
   - Créer des backups automatiques de vos fichiers .dat ( en .backup) pour éviter toutes corruptions si erreurs
   - Transformer la structure des Pokémon
   - Copier vos Pokémon vers le nouveau monde

### Étape 4 : Vérifier dans le jeu

 Lancez **Minecraft** avec **Cobblemon Academy 7**
2. Chargez votre **nouveau monde**
3. Ouvrez votre **PC** et vérifiez que vos Pokémon sont là !
