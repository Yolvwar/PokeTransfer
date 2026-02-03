# Guide Simple - Transférer vos Pokémon entre versions Cobblemon

**Ce guide vous aide à transférer vos Pokémon du PC de Cobblemon Academy 2.0 vers Cobblemon 1.7**

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

### Étape 1 : Récupérer le dossier pokemon/

Vous devez récupérer le dossier `pokemon/` depuis votre ancien monde (solo ou serveur).

#### Si vous jouez en solo :

1. Ouvrez le **Launcher CurseForge**
2. Faites un **clic droit** sur votre ModPack (ex: Cobblemon Academy 2.0)
3. Cliquez sur "**Ouvrir le dossier**"
4. Naviguez vers : `saves` → nom de votre monde (ex: world)
5. Vous verrez le dossier **pokemon/** → **Copiez-le**

#### Si vous jouez sur un serveur :

1. Connectez-vous à votre serveur (FTP, SFTP, ou panneau de contrôle)
2. Allez dans les fichiers de votre serveur
3. Cherchez le dossier **world/**
4. À l'intérieur, trouvez le dossier **pokemon/**
5. **Téléchargez** ce dossier sur votre ordinateur

**Le dossier pokemon/ doit contenir :**
- `pcstore/` (vos Pokémon dans le PC)
- `playerpartystore/` (vos Pokémon dans votre équipe)

---

### Étape 2 : Lancer le script de conversion

1. Ouvrez un **PowerShell** ou **Invite de commandes** ou se trouve le script convert_pokemon_gui.py

2. Lancez le script :
   ```powershell
   python convert_pokemon_gui.py
   ```

3. Une fenêtre s'ouvre :
   - Cliquez sur **"Parcourir"**
   - Sélectionnez le dossier **pokemon/** que vous avez récupéré
   - Le script détecte automatiquement les fichiers à convertir
   - Cliquez sur **"Lancer la conversion"**

4. Le script va :
   - Créer des **backups automatiques** (.backup) de tous vos fichiers
   - Transformer la structure des Pokémon (IVs, Features, data_version)
   - Modifier les fichiers **sur place** dans le dossier pokemon/

---

### Étape 3 : Transférer le dossier converti

#### Si vous jouez en solo :

1. Ouvrez le **Launcher CurseForge**
2. Faites un **clic droit** sur votre **nouveau modpack** (ex: "Cacademy v2")
3. Cliquez sur "**Ouvrir le dossier**"
4. Naviguez vers : `saves` → votre nouveau monde
5. **Remplacez** le dossier **pokemon/** existant par votre dossier converti

#### Si vous jouez sur un serveur :

1. Connectez-vous à votre serveur (FTP, SFTP, ou panneau de contrôle)
2. Allez dans `world/`
3. **Supprimez** l'ancien dossier **pokemon/**
4. **Uploadez** votre dossier **pokemon/** converti

---

### Étape 4 : Vérifier dans le jeu

1. Lancez **Minecraft** avec votre nouveau Modpack
2. Chargez votre **monde**
3. Ouvrez votre **PC** et vérifiez que vos Pokémon sont là !
4. Vérifiez aussi votre **équipe**

**En cas de problème :**
- Les fichiers `.backup` sont dans le même dossier que vos fichiers originaux
- Renommez-les en `.dat` pour restaurer vos données originales