import os
from config import TEXTURE_MAPPING, DEFAULT_PARAMETERS

def process_texture_folder(folder_path):
    textures = {}
    base_name = os.path.basename(folder_path)

    # Options activées en fonction des textures trouvées
    options = {
        "F_SPECULAR": False,
        "F_SELF_ILLUM": False,
        "F_METALNESS_TEXTURE": False,
    }

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
