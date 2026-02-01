"""
CONVERTISSEUR POKÉMON - v2.0 → v1.7
Interface pour utilisateur
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
from nbtlib import nbt, Int, Byte, String, Compound, List
import shutil
from pathlib import Path
import threading

class PokemonConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertisseur Pokémon Cobblemon")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f5f5")
        
        self.pokemon_folder_path = tk.StringVar()
        self.is_converting = False
        
        self.create_widgets()
        
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#ffffff", pady=35)
        header_frame.pack(fill="x")
        
        title = tk.Label(
            header_frame,
            text="Convertisseur Pokémon",
            font=("Segoe UI", 26, "normal"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        title.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="Cobblemon Academy 2.0 → 1.7",
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        subtitle.pack(pady=(8, 0))
        
        subtitle2 = tk.Label(
            header_frame,
            text="Sélectionnez le dossier pokemon/ de votre ancien monde",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#95a5a6"
        )
        subtitle2.pack(pady=(4, 0))
        
        separator = tk.Frame(self.root, height=1, bg="#e0e0e0")
        separator.pack(fill="x")
        
        main_frame = tk.Frame(self.root, padx=40, pady=30, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True)
        
        tk.Label(
            main_frame,
            text="Dossier pokemon/ de l'ancien monde (v2.0)",
            font=("Segoe UI", 10, "normal"),
            bg="#f5f5f5",
            fg="#34495e"
        ).pack(anchor="w", pady=(0, 8))
        
        pokemon_frame = tk.Frame(main_frame, bg="#f5f5f5")
        pokemon_frame.pack(fill="x", pady=(0, 25))
        
        entry_pokemon = tk.Entry(
            pokemon_frame,
            textvariable=self.pokemon_folder_path,
            font=("Segoe UI", 10),
            state="readonly",
            bg="#ffffff",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        entry_pokemon.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)
        
        btn_pokemon = tk.Button(
            pokemon_frame,
            text="Parcourir",
            command=self.browse_pokemon_folder,
            bg="#3498db",
            fg="#ffffff",
            font=("Segoe UI", 10, "normal"),
            padx=25,
            pady=9,
            relief="flat",
            cursor="hand2",
            borderwidth=0,
            activebackground="#2980b9",
            activeforeground="#ffffff"
        )
        btn_pokemon.pack(side="right")
        btn_pokemon.bind("<Enter>", lambda e: btn_pokemon.config(bg="#2980b9"))
        btn_pokemon.bind("<Leave>", lambda e: btn_pokemon.config(bg="#3498db"))
        
        # Info box
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", relief="solid", borderwidth=1)
        info_frame.pack(fill="x", pady=(0, 35), padx=5)
        
        info_text = tk.Label(
            info_frame,
            text="ℹ️ Le dossier doit contenir pcstore/ et playerpartystore/\nUn backup automatique sera créé avant conversion",
            font=("Segoe UI", 9),
            bg="#e8f4f8",
            fg="#2c3e50",
            justify="left"
        )
        info_text.pack(pady=12, padx=15)
        
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(0, 25))
        
        self.convert_button = tk.Button(
            button_frame,
            text="Lancer la conversion",
            command=self.start_conversion,
            bg="#27ae60",
            fg="#ffffff",
            font=("Segoe UI", 12, "normal"),
            pady=15,
            relief="flat",
            cursor="hand2",
            borderwidth=0,
            activebackground="#229954",
            activeforeground="#ffffff"
        )
        self.convert_button.pack(fill="x")
        self.convert_button.bind("<Enter>", lambda e: self.convert_button.config(bg="#229954") if self.convert_button['state'] == 'normal' else None)
        self.convert_button.bind("<Leave>", lambda e: self.convert_button.config(bg="#27ae60") if self.convert_button['state'] == 'normal' else None)
        
        self.progress = ttk.Progressbar(
            main_frame,
            mode="indeterminate",
            length=300
        )
        self.progress.pack(fill="x", pady=(0, 25))
        
        tk.Label(
            main_frame,
            text="Journal de conversion",
            font=("Segoe UI", 10, "normal"),
            bg="#f5f5f5",
            fg="#34495e"
        ).pack(anchor="w", pady=(0, 8))
        
        log_frame = tk.Frame(main_frame, bg="#ffffff", padx=1, pady=1)
        log_frame.pack(fill="both", expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=14,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#2c3e50",
            wrap="word",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        self.log_text.pack(fill="both", expand=True, padx=0, pady=0)
        
        separator_bottom = tk.Frame(self.root, height=1, bg="#e0e0e0")
        separator_bottom.pack(fill="x", side="bottom")
        
        footer_frame = tk.Frame(self.root, bg="#ffffff", pady=15)
        footer_frame.pack(fill="x", side="bottom")
        
        instructions = tk.Label(
            footer_frame,
            text="Sélectionnez votre dossier pokemon/, puis lancez la conversion",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#95a5a6"
        )
        instructions.pack()
        
    def browse_pokemon_folder(self):
        path = filedialog.askdirectory(
            title="Sélectionner le dossier pokemon/ (contenant pcstore et playerpartystore)"
        )
        if path:
            pokemon_path = Path(path)
            # Vérifier que les sous-dossiers existent
            if (pokemon_path / "pcstore").exists() or (pokemon_path / "playerpartystore").exists():
                self.pokemon_folder_path.set(path)
                self.log(f"[OK] Dossier pokemon: {path}")
                
                # Afficher ce qui a été trouvé
                if (pokemon_path / "pcstore").exists():
                    pcstore_files = len(list((pokemon_path / "pcstore").rglob("*.dat")))
                    self.log(f"    → pcstore: {pcstore_files} fichiers trouvés")
                if (pokemon_path / "playerpartystore").exists():
                    playerparty_files = len(list((pokemon_path / "playerpartystore").rglob("*.dat")))
                    self.log(f"    → playerpartystore: {playerparty_files} fichiers trouvés")
            else:
                messagebox.showerror(
                    "Erreur",
                    "Le dossier sélectionné ne contient pas pcstore/ ou playerpartystore/\n\n"
                    "Veuillez sélectionner le dossier pokemon/ qui contient ces sous-dossiers."
                )
                self.log(f"[ERREUR] Dossier invalide: {path}")
            
    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update()
        
    def start_conversion(self):
        if not self.pokemon_folder_path.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner le dossier pokemon/")
            return
            
        if self.is_converting:
            messagebox.showwarning("Attention", "Une conversion est déjà en cours")
            return
            
        result = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment convertir les Pokémon?\n\n"
            "⚠️ Les fichiers seront modifiés sur place\n"
            "Un backup (.backup) sera créé automatiquement\n\n"
            "Assurez-vous d'avoir une copie de sauvegarde!"
        )
        
        if not result:
            return
            
        self.is_converting = True
        self.convert_button.config(state="disabled", text="Conversion en cours...", bg="#95a5a6")
        self.progress.start()
        self.log_text.delete(1.0, "end")
        
        thread = threading.Thread(target=self.convert_pokemon)
        thread.daemon = True
        thread.start()
        
    def convert_pokemon(self):
        try:
            pokemon_folder = Path(self.pokemon_folder_path.get())
            
            subfolders = ["pcstore", "playerpartystore"]
            
            total_pokemon = 0
            total_transformed = 0
            
            self.log("=" * 70)
            self.log("DÉBUT DE LA CONVERSION")
            self.log("=" * 70)
            self.log(f"Dossier: {pokemon_folder}\n")
            
            for subfolder in subfolders:
                folder_path = pokemon_folder / subfolder
                
                self.log(f"\n[Traitement] {subfolder}/")
                self.log("-" * 70)
                
                if not folder_path.exists():
                    self.log(f"  [INFO] Dossier non trouvé, passage au suivant")
                    continue
                
                dat_files = list(folder_path.rglob("*.dat"))
                
                if not dat_files:
                    self.log(f"  [INFO] Aucun fichier .dat trouvé")
                    continue
                
                self.log(f"  Fichiers trouvés: {len(dat_files)}")
                
                for dat_file in dat_files:
                    try:
                        relative_path = dat_file.relative_to(folder_path)
                        
                        # Backup automatique
                        backup_path = str(dat_file) + '.backup'
                        if not Path(backup_path).exists():
                            shutil.copy2(dat_file, backup_path)
                            self.log(f"  [Backup] {relative_path}.backup créé")
                        
                        data = nbt.load(str(dat_file))
                        file_modified = False
                        
                        # Traiter les Box (pcstore)
                        for box_key in list(data.keys()):
                            if box_key.startswith('Box'):
                                box = data[box_key]
                                
                                if not hasattr(box, 'keys'):
                                    continue
                                
                                if 'BoxWallpaper' in box:
                                    del box['BoxWallpaper']
                                    file_modified = True
                                
                                for slot_key in list(box.keys()):
                                    if slot_key.startswith('Slot'):
                                        pokemon = box[slot_key]
                                        
                                        if hasattr(pokemon, 'keys'):
                                            species = pokemon.get('Species', 'Unknown')
                                            level = pokemon.get('Level', '?')
                                            
                                            self.log(f"  [Pokemon] {species} (Niv.{level}) - {box_key}/{slot_key}")
                                            
                                            if self.transform_pokemon(pokemon):
                                                file_modified = True
                                                total_transformed += 1
                                            
                                            total_pokemon += 1
                        
                        # Traiter les Slots directs (playerpartystore)
                        for slot_key in list(data.keys()):
                            if slot_key.startswith('Slot'):
                                pokemon = data[slot_key]
                                
                                if hasattr(pokemon, 'keys') and 'Species' in pokemon:
                                    species = pokemon.get('Species', 'Unknown')
                                    level = pokemon.get('Level', '?')
                                    
                                    self.log(f"  [Pokemon] {species} (Niv.{level}) - {slot_key}")
                                    
                                    if self.transform_pokemon(pokemon):
                                        file_modified = True
                                        total_transformed += 1
                                    
                                    total_pokemon += 1
                        
                        if file_modified:
                            data.save(str(dat_file))
                            self.log(f"  [Sauvegarde] {relative_path}")
                        else:
                            self.log(f"  [Info] Aucune modification nécessaire")
                        
                    except Exception as e:
                        self.log(f"  [ERREUR] {relative_path}: {e}")
            
            self.log("\n" + "=" * 70)
            self.log("RÉSUMÉ DE LA CONVERSION")
            self.log("=" * 70)
            self.log(f"  Pokémon traités:     {total_pokemon}")
            self.log(f"  Pokémon transformés: {total_transformed}")
            self.log("=" * 70)
            
            messagebox.showinfo(
                "Succès",
                f"Conversion terminée avec succès!\n\n"
                f"Pokémon traités: {total_pokemon}\n"
                f"Pokémon transformés: {total_transformed}\n\n"
                f"Les fichiers .backup ont été créés\n"
                f"Vous pouvez maintenant utiliser ce dossier dans votre monde 1.7"
            )
            
        except Exception as e:
            self.log(f"\n[ERREUR CRITIQUE] {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la conversion:\n{e}")
            
        finally:
            self.is_converting = False
            self.convert_button.config(state="normal", text="Lancer la conversion", bg="#27ae60")
            self.progress.stop()
    
    def transform_pokemon(self, pokemon):
        transformed = False
        species = pokemon.get('Species', '')
        
        # Transformation des IVs
        if 'IVs' in pokemon:
            ivs = pokemon['IVs']
            
            if hasattr(ivs, 'keys') and 'Base' in ivs:
                base = ivs['Base']
                new_ivs = Compound({})
                if hasattr(base, 'keys'):
                    for stat_key, stat_value in base.items():
                        new_ivs[stat_key] = stat_value
                
                pokemon['IVs'] = new_ivs
                transformed = True
                self.log(f"      [OK] IVs transformés")
            
            # Vérifier HyperTrained après avoir potentiellement remplacé IVs
            if hasattr(pokemon['IVs'], 'keys') and 'HyperTrained' in pokemon['IVs']:
                del pokemon['IVs']['HyperTrained']
                self.log(f"      [OK] HyperTrained supprimé")
        
        keys_to_remove = ['HeldItemDroppableByAI', 'HeldItemVisible']
        for key in keys_to_remove:
            if key in pokemon:
                del pokemon[key]
                transformed = True
        
        # Data version
        if 'cobblemon:data_version' in pokemon:
            if pokemon['cobblemon:data_version'] != 1:
                pokemon['cobblemon:data_version'] = Int(1)
                transformed = True
                self.log(f"      [OK] data_version -> 1")
        else:
            pokemon['cobblemon:data_version'] = Int(1)
            transformed = True
            self.log(f"      [OK] data_version ajouté")
        
        if 'unown' in str(species).lower():
            form_id = pokemon.get('FormId', '')
            
            if form_id:
                self.log(f"      [Zarbi] Forme: {form_id}")
                
                old_features = pokemon.get('Features', [])
                character_value = form_id
                
                for feat in old_features:
                    if hasattr(feat, 'keys') and 'character' in feat:
                        character_value = str(feat['character'])
                        break
                
                new_features = List[Compound]([
                    Compound({
                        'cobblemon:feature_id': String('letter'),
                        'letter': String(character_value if character_value else 'a')
                    }),
                    Compound({
                        'cobblemon:feature_id': String('ender'),
                        'ender': Byte(0)
                    }),
                    Compound({
                        'cobblemon:feature_id': String('fertility'),
                        'fertility': Int(8)
                    }),
                    Compound({
                        'cobblemon:feature_id': String('dynamax_level'),
                        'dynamax_level': Int(0)
                    }),
                    Compound({
                        'cobblemon:feature_id': String('radiant'),
                        'radiant': String('regular')
                    }),
                    Compound({
                        'cobblemon:feature_id': String('character'),
                        'character': String(character_value if character_value else 'a')
                    })
                ])
                
                pokemon['Features'] = new_features
                transformed = True
                self.log(f"      [OK] Features Zarbi reconstruits")
        else:
            # TOUS les autres Pokémon doivent avoir fertility, dynamax_level, radiant
            if 'Features' not in pokemon or not pokemon['Features']:
                # Créer les features de base
                new_features = List[Compound]([
                    Compound({
                        'cobblemon:feature_id': String('fertility'),
                        'fertility': Int(8)
                    }),
                    Compound({
                        'cobblemon:feature_id': String('dynamax_level'),
                        'dynamax_level': Int(0)
                    }),
                    Compound({
                        'cobblemon:feature_id': String('radiant'),
                        'radiant': String('regular')
                    })
                ])
                pokemon['Features'] = new_features
                transformed = True
                self.log(f"      [OK] Features de base ajoutés")
            else:
                existing_features = pokemon['Features']
                feature_ids = set()
                
                for feat in existing_features:
                    if hasattr(feat, 'keys') and 'cobblemon:feature_id' in feat:
                        feature_ids.add(str(feat['cobblemon:feature_id']))
                
                required_features = {'fertility', 'dynamax_level', 'radiant'}
                missing_features = required_features - feature_ids
                
                if missing_features:
                    features_list = list(existing_features)
                    
                    if 'fertility' in missing_features:
                        features_list.append(Compound({
                            'cobblemon:feature_id': String('fertility'),
                            'fertility': Int(8)
                        }))
                    
                    if 'dynamax_level' in missing_features:
                        features_list.append(Compound({
                            'cobblemon:feature_id': String('dynamax_level'),
                            'dynamax_level': Int(0)
                        }))
                    
                    if 'radiant' in missing_features:
                        features_list.append(Compound({
                            'cobblemon:feature_id': String('radiant'),
                            'radiant': String('regular')
                        }))
                    
                    pokemon['Features'] = List[Compound](features_list)
                    transformed = True
                    self.log(f"      [OK] Features manquantes ajoutées: {missing_features}")
        
        # Vérification et préservation des formes spéciales
        if 'FormId' in pokemon:
            form = pokemon['FormId']
            if form and form != 'normal':
                self.log(f"      [INFO] Forme spéciale préservée: {form}")
        
        return transformed

def main():
    root = tk.Tk()
    app = PokemonConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
