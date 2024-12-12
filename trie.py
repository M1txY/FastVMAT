import os
import shutil

def organize_textures_by_prefix(folder_path):
    # Vérifie si le dossier existe
    if not os.path.exists(folder_path):
        print(f"Le dossier {folder_path} n'existe pas.")
        return

    # Liste tous les fichiers dans le dossier
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    for file in files:
        # Identifie le préfixe du fichier
        prefix = "_".join(file.split("_")[:2])
        
        # Crée un sous-dossier pour ce préfixe si nécessaire
        subfolder_path = os.path.join(folder_path, prefix)
        os.makedirs(subfolder_path, exist_ok=True)
        
        # Déplace le fichier dans le sous-dossier
        source = os.path.join(folder_path, file)
        destination = os.path.join(subfolder_path, file)
        shutil.move(source, destination)
    
    print(f"Organisation terminée dans le dossier {folder_path}")

# Exemple d'utilisation
folder_path = "texture_opera"  # Remplacez par le chemin vers votre dossier
organize_textures_by_prefix(folder_path)
