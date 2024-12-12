import os
import shutil

def organize_textures_by_prefix(folder_path):
    if not os.path.exists(folder_path):
        print(f"Le dossier {folder_path} n'existe pas.")
        return
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    for file in files:
        prefix = "_".join(file.split("_")[:2])
        
        subfolder_path = os.path.join(folder_path, prefix)
        os.makedirs(subfolder_path, exist_ok=True)
        
        source = os.path.join(folder_path, file)
        destination = os.path.join(subfolder_path, file)
        shutil.move(source, destination)
    
    print(f"Organisation terminée dans le dossier {folder_path}")

folder_path = "Textures" 
organize_textures_by_prefix(folder_path)
