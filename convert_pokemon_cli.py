"""
CONVERTISSEUR POKÉMON - v2.0 → v1.7
Version CLI (ligne de commande)
Peut être exécuté sur serveur ou en local
"""

from nbtlib import nbt, Int, Byte, String, Compound, List
import shutil
from pathlib import Path
import sys

def log(message):
    """Affiche et log un message"""
    print(message)
    sys.stdout.flush()

def transform_pokemon(pokemon):
    """Transforme un Pokémon pour la compatibilité v1.7"""
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
            log(f"      [OK] IVs transformés")
        
        if hasattr(pokemon['IVs'], 'keys') and 'HyperTrained' in pokemon['IVs']:
            del pokemon['IVs']['HyperTrained']
            log(f"      [OK] HyperTrained supprimé")
    
    keys_to_remove = ['HeldItemDroppableByAI', 'HeldItemVisible']
    for key in keys_to_remove:
        if key in pokemon:
            del pokemon[key]
            transformed = True
    
    if 'cobblemon:data_version' in pokemon:
        if pokemon['cobblemon:data_version'] != 1:
            pokemon['cobblemon:data_version'] = Int(1)
            transformed = True
            log(f"      [OK] data_version -> 1")
    else:
        pokemon['cobblemon:data_version'] = Int(1)
        transformed = True
        log(f"      [OK] data_version ajouté")
    
    if 'unown' in str(species).lower():
        form_id = pokemon.get('FormId', '')
        
        if form_id:
            log(f"      [Zarbi] Forme: {form_id}")
            
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
            log(f"      [OK] Features Zarbi reconstruits")
    else:
        if 'Features' not in pokemon or not pokemon['Features']:
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
            log(f"      [OK] Features de base ajoutés")
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
                log(f"      [OK] Features manquantes ajoutées: {missing_features}")
    
    if 'FormId' in pokemon:
        form = pokemon['FormId']
        if form and form != 'normal':
            log(f"      [INFO] Forme spéciale préservée: {form}")
    
    return transformed

def convert_pokemon_folder(pokemon_folder_path):
    """Convertit tous les Pokémon dans le dossier pokemon/"""
    
    pokemon_folder = Path(pokemon_folder_path)
    
    if not pokemon_folder.exists():
        log(f"[ERREUR] Le dossier n'existe pas: {pokemon_folder}")
        return False
    
    has_pcstore = (pokemon_folder / "pcstore").exists()
    has_playerparty = (pokemon_folder / "playerpartystore").exists()
    
    if not has_pcstore and not has_playerparty:
        log(f"[ERREUR] Le dossier ne contient ni pcstore/ ni playerpartystore/")
        return False
    
    subfolders = []
    if has_pcstore:
        subfolders.append("pcstore")
    if has_playerparty:
        subfolders.append("playerpartystore")
    
    total_pokemon = 0
    total_transformed = 0
    
    log("=" * 90)
    log("CONVERTISSEUR POKÉMON COBBLEMON 2.0 -> 1.7")
    log("=" * 90)
    log(f"Dossier: {pokemon_folder}\n")
    
    for subfolder in subfolders:
        folder_path = pokemon_folder / subfolder
        
        log(f"\n[Traitement] {subfolder}/")
        log("-" * 90)
        
        if not folder_path.exists():
            log(f"  [INFO] Dossier non trouvé, passage au suivant")
            continue
        
        dat_files = list(folder_path.rglob("*.dat"))
        
        if not dat_files:
            log(f"  [INFO] Aucun fichier .dat trouvé")
            continue
        
        log(f"  Fichiers trouvés: {len(dat_files)}")
        
        for dat_file in dat_files:
            try:
                relative_path = dat_file.relative_to(folder_path)
                
                backup_path = str(dat_file) + '.backup'
                if not Path(backup_path).exists():
                    shutil.copy2(dat_file, backup_path)
                    log(f"  [Backup] {relative_path}.backup créé")
                
                data = nbt.load(str(dat_file))
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
                                    
                                    log(f"  [Pokemon] {species} (Niv.{level}) - {box_key}/{slot_key}")
                                    
                                    if transform_pokemon(pokemon):
                                        file_modified = True
                                        total_transformed += 1
                                    
                                    total_pokemon += 1
                
                for slot_key in list(data.keys()):
                    if slot_key.startswith('Slot'):
                        pokemon = data[slot_key]
                        
                        if hasattr(pokemon, 'keys') and 'Species' in pokemon:
                            species = pokemon.get('Species', 'Unknown')
                            level = pokemon.get('Level', '?')
                            
                            log(f"  [Pokemon] {species} (Niv.{level}) - {slot_key}")
                            
                            if transform_pokemon(pokemon):
                                file_modified = True
                                total_transformed += 1
                            
                            total_pokemon += 1
                
                if file_modified:
                    data.save(str(dat_file))
                    log(f"  [Sauvegarde] {relative_path}")
                else:
                    log(f"  [Info] Aucune modification nécessaire")
                
            except Exception as e:
                log(f"  [ERREUR] {relative_path}: {e}")
                import traceback
                traceback.print_exc()
    
    log("\n" + "=" * 90)
    log("RÉSUMÉ DE LA CONVERSION")
    log("=" * 90)
    log(f"  Pokémon traités:     {total_pokemon}")
    log(f"  Pokémon transformés: {total_transformed}")
    log("=" * 90)
    log("\nConversion terminée avec succès!")
    log("Les fichiers .backup ont été créés pour sécurité.")
    
    return True

def main():
    """Point d'entrée principal"""
    
    if len(sys.argv) > 1:
        pokemon_folder = sys.argv[1]
    else:
        log("=" * 90)
        log("CONVERTISSEUR POKÉMON COBBLEMON 2.0 -> 1.7 (CLI)")
        log("=" * 90)
        log("\nEntrez le chemin du dossier pokemon/ à convertir:")
        log("(Le dossier doit contenir pcstore/ et/ou playerpartystore/)\n")
        
        pokemon_folder = input("Chemin: ").strip().strip('"\'')
    
    if not pokemon_folder:
        log("\n[ERREUR] Aucun chemin fourni.")
        log("\nUtilisation:")
        log("  python convert_pokemon_cli.py [chemin_dossier_pokemon]")
        log("\nExemple:")
        log('  python convert_pokemon_cli.py "C:/Users/Username/Downloads/pokemon"')
        sys.exit(1)
    
    success = convert_pokemon_folder(pokemon_folder)
    
    if not success:
        sys.exit(1)
    
    log("\nAppuyez sur Entrée pour quitter...")
    input()

if __name__ == "__main__":
    main()