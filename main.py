import os
import shutil
import subprocess
from PIL import Image
from config import TEXTURE_MAPPING, DEFAULT_PARAMETERS

def extract_uasset_to_png(umodel_path, folder_path):
    """
    Extrait les textures des fichiers .uasset et remplace les fichiers par des .png.
    """
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".uasset"):
            input_path = os.path.abspath(os.path.join(folder_path, file_name))
            command = [
                umodel_path,
                "-export",
                input_path
            ]
            try:
                print(f"Extraction des textures de : {file_name}")
                subprocess.run(command, check=True, cwd=folder_path)
                print(f"Textures extraites pour : {file_name}")

                # Localiser le dossier "UmodelExport"
                export_folder = os.path.join(folder_path, "UmodelExport")
                if os.path.exists(export_folder):
                    convert_and_move_tga_to_png(export_folder, folder_path)
                    shutil.rmtree(export_folder)  # Supprimer le dossier UmodelExport après traitement
                    print(f"Supprimé : {export_folder}")

                # Supprimer le fichier .uasset après extraction
                os.remove(input_path)
                print(f"Supprimé : {file_name}")

            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'extraction pour {file_name}: {e}")

def convert_and_move_tga_to_png(source_folder, target_folder):
    """
    Convertit les fichiers .tga en .png et les déplace dans le dossier cible.
    """
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".tga"):
            tga_path = os.path.join(source_folder, file_name)
            png_path = os.path.join(target_folder, file_name.replace(".tga", ".png"))
            try:
                with Image.open(tga_path) as img:
                    img.save(png_path, format="PNG")
                    print(f"Converti et déplacé : {tga_path} -> {png_path}")
            except Exception as e:
                print(f"Erreur lors de la conversion de {tga_path} : {e}")

def process_texture_folder(folder_path):
    """
    Traite un dossier pour générer un fichier .vmat à partir des textures.
    """
    textures = {}
    base_name = os.path.basename(folder_path)

    # Options activées en fonction des textures trouvées
    options = {
        "F_SPECULAR": False,
        "F_SELF_ILLUM": False,
        "F_METALNESS_TEXTURE": False,
    }

    # Extraire les textures des fichiers .uasset
    umodel_path = os.path.abspath("umodel_64.exe")
    extract_uasset_to_png(umodel_path, folder_path)

    # Traiter les fichiers de texture
    for file in os.listdir(folder_path):
        if file.endswith((".png", ".jpg", ".jpeg", ".tga")):
            for texture_key, suffix_list in TEXTURE_MAPPING.items():
                if any(suffix in file.lower() for suffix in suffix_list):
                    relative_path = os.path.join(
                        "materials",
                        os.path.relpath(folder_path, "materials"),
                        file
                    ).replace("\\", "/")
                    textures[texture_key] = relative_path

                    # Active les options en fonction des types de texture détectés
                    if texture_key == "TextureSelfIllumMask":
                        options["F_SELF_ILLUM"] = True
                    if texture_key == "TextureMetalness":
                        options["F_METALNESS_TEXTURE"] = True
                    if texture_key == "TextureSpecular":
                        options["F_SPECULAR"] = True
                    break

    # Contenu du fichier .vmat
    vmat_content = ["// THIS FILE IS AUTO-GENERATED\n", "Layer0\n{\n"]
    vmat_content.append(f'\tshader "{DEFAULT_PARAMETERS["shader"]}"\n\n')

    # Ajoute les options activées
    for option, enabled in options.items():
        if enabled:
            vmat_content.append(f"\t{option} 1\n")
    if not options["F_METALNESS_TEXTURE"]:
        vmat_content.append('\tg_flMetalness "0.000"\n')

    # Ajoute les paramètres par défaut
    for param, value in DEFAULT_PARAMETERS.items():
        vmat_content.append(f'\t{param} "{value}"\n')

    # Ajoute les textures détectées
    for texture_key, texture_path in textures.items():
        vmat_content.append(f'\t{texture_key} "{texture_path}"\n')

    vmat_content.append("}\n")

    # Génère le fichier .vmat
    vmat_file_path = os.path.join(folder_path, f"{base_name}.vmat")
    with open(vmat_file_path, "w") as vmat_file:
        vmat_file.writelines(vmat_content)
    print(f"Generated: {vmat_file_path}")

def main():
    root_folder = "materials"
    if not os.path.exists(root_folder):
        print(f"Le dossier '{root_folder}' est introuvable.")
        return

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            process_texture_folder(folder_path)

if __name__ == "__main__":
    main()
