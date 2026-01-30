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
        
        self.old_world_path = tk.StringVar()
        self.new_world_path = tk.StringVar()
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
            text="Cobblemon Academy 2.0 vers 1.7",
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        subtitle.pack(pady=(8, 0))
        
        separator = tk.Frame(self.root, height=1, bg="#e0e0e0")
        separator.pack(fill="x")
        
        main_frame = tk.Frame(self.root, padx=40, pady=30, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True)
        
        tk.Label(
            main_frame,
            text="Monde source",
            font=("Segoe UI", 10, "normal"),
            bg="#f5f5f5",
            fg="#34495e"
        ).pack(anchor="w", pady=(0, 8))
        
        old_frame = tk.Frame(main_frame, bg="#f5f5f5")
        old_frame.pack(fill="x", pady=(0, 25))
        
        entry_old = tk.Entry(
            old_frame,
            textvariable=self.old_world_path,
            font=("Segoe UI", 10),
            state="readonly",
            bg="#ffffff",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        entry_old.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)
        
        btn_old = tk.Button(
            old_frame,
            text="Parcourir",
            command=self.browse_old_world,
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
        btn_old.pack(side="right")
        btn_old.bind("<Enter>", lambda e: btn_old.config(bg="#2980b9"))
        btn_old.bind("<Leave>", lambda e: btn_old.config(bg="#3498db"))
        
        tk.Label(
            main_frame,
            text="Monde destination",
            font=("Segoe UI", 10, "normal"),
            bg="#f5f5f5",
            fg="#34495e"
        ).pack(anchor="w", pady=(0, 8))
        
        new_frame = tk.Frame(main_frame, bg="#f5f5f5")
        new_frame.pack(fill="x", pady=(0, 35))
        
        entry_new = tk.Entry(
            new_frame,
            textvariable=self.new_world_path,
            font=("Segoe UI", 10),
            state="readonly",
            bg="#ffffff",
            fg="#2c3e50",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        entry_new.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)
        
        btn_new = tk.Button(
            new_frame,
            text="Parcourir",
            command=self.browse_new_world,
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
        btn_new.pack(side="right")
        btn_new.bind("<Enter>", lambda e: btn_new.config(bg="#2980b9"))
        btn_new.bind("<Leave>", lambda e: btn_new.config(bg="#3498db"))
        
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
            text="Sélectionnez les deux dossiers de monde, puis lancez la conversion",
            font=("Segoe UI", 9),
            bg="#ffffff",
            fg="#95a5a6"
        )
        instructions.pack()
        
    def browse_old_world(self):
        path = filedialog.askdirectory(
            title="Sélectionner le dossier du monde Cobblemon 2.0"
        )
        if path:
            self.old_world_path.set(path)
            self.log(f"[OK] Monde source: {path}")
            
    def browse_new_world(self):
        path = filedialog.askdirectory(
            title="Sélectionner le dossier du monde Cobblemon 1.7"
        )
        if path:
            self.new_world_path.set(path)
            self.log(f"[OK] Monde destination: {path}")
            
    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.root.update()
        
    def start_conversion(self):
        if not self.old_world_path.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner le monde source (2.0)")
            return
            
        if not self.new_world_path.get():
            messagebox.showerror("Erreur", "Veuillez sélectionner le monde destination (1.7)")
            return
            
        if self.is_converting:
            messagebox.showwarning("Attention", "Une conversion est déjà en cours")
            return
            
        result = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment convertir les Pokémon?\n\n"
            "Un backup sera créé automatiquement."
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
            old_world = self.old_world_path.get()
            new_world = self.new_world_path.get()
            
            folders = [
                "pokemon/pcstore",
                "pokemon/playerpartystore",
            ]
            
            total_pokemon = 0
            total_transformed = 0
            
            self.log("=" * 70)
            self.log("DÉBUT DE LA CONVERSION")
            self.log("=" * 70)
            
            for folder in folders:
                old_folder = Path(old_world) / folder
                new_folder = Path(new_world) / folder
                
                self.log(f"\n[Traitement] {folder}")
                self.log("-" * 70)
                
                if not old_folder.exists():
                    self.log(f"  [ATTENTION] Dossier source non trouvé")
                    continue
                
                dat_files = list(old_folder.rglob("*.dat"))
                
                if not dat_files:
                    self.log(f"  [INFO] Aucun fichier .dat trouvé")
                    continue
                
                for old_file in dat_files:
                    try:
                        relative_path = old_file.relative_to(old_folder)
                        new_file = new_folder / relative_path
                        
                        new_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Backup
                        if new_file.exists():
                            backup_path = str(new_file) + '.backup'
                            if not Path(backup_path).exists():
                                shutil.copy2(new_file, backup_path)
                        
                        data = nbt.load(str(old_file))
                        file_modified = False
                        
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
                        
                        if file_modified:
                            data.save(str(new_file))
                            self.log(f"  [Sauvegarde] {relative_path}")
                        
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
                f"Conversion terminée!\n\n"
                f"Pokémon traités: {total_pokemon}\n"
                f"Pokémon transformés: {total_transformed}\n\n"
                f"Vous pouvez maintenant lancer votre monde 1.7"
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
        
        # Features pour Zarbi/Unown
        if 'unown' in str(species).lower():
            form_id = pokemon.get('FormId', '')
            
            if form_id:
                self.log(f"      [Zarbi] Forme: {form_id}")
                
                if 'Features' in pokemon:
                    old_features = pokemon['Features']
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
        
        # Vérification et préservation des formes spéciales
        elif 'FormId' in pokemon:
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
