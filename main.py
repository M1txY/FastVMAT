import os

# Mapping des textures et suffixes
texture_mapping = {
    "TextureColor": ["_albedo", "_diffuse", "_basecolor", "_color", "_col", "_bc", "_diff"],
    "TextureAmbientOcclusion": ["_ao", "_ambientocclusion", "_occlusion", "_ambocc", "_aoc", "_occl"],
    "TextureNormal": ["_normal", "_nor", "_norm", "_nrm", "_normalmap", "_nml", "_bump"],
    "TextureRoughness": ["_roughness", "_rou", "_rgh", "_gloss", "_gls", "_rough", "_specular"],
    "TextureMetalness": ["_metallic", "_met", "_metal", "_mtl", "_metalness", "_metall"],
    "TextureSelfIllumMask": ["_selfillum", "_illum", "_glowmask", "_emit", "_emissive", "_light"],
    "TextureTranslucency": ["_translucent", "_trans", "_opacity", "_opa", "_alpha"],
}

# Paramètres par défaut
default_parameters = {
    "shader": "complex.shader",
    "g_flAmbientOcclusionDirectDiffuse": "0.000",
    "g_flAmbientOcclusionDirectSpecular": "0.000",
    "g_flModelTintAmount": "1.000",
    "g_vColorTint": "[1.000000 1.000000 1.000000 0.000000]",
    "g_flFadeExponent": "1.000",
    "g_bFogEnabled": "1",
    "g_flRoughnessScaleFactor": "1.000",
    "g_nScaleTexCoordUByModelScaleAxis": "0",
    "g_nScaleTexCoordVByModelScaleAxis": "0",
    "g_vTexCoordOffset": "[0.000 0.000]",
    "g_vTexCoordScale": "[1.000 1.000]",
    "g_vTexCoordScrollSpeed": "[0.000 0.000]",
}

def process_texture_folder(folder_path, suffixes):
    """Traite un dossier pour générer un fichier .vmat basé sur les textures détectées."""
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
            for texture_key, suffix_list in texture_mapping.items():
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
    vmat_content.append(f'\tshader "{default_parameters["shader"]}"\n\n')

    # Ajoute les options activées
    for option, enabled in options.items():
        if enabled:
            vmat_content.append(f"\t{option} 1\n")
    if not options["F_METALNESS_TEXTURE"]:
        vmat_content.append('\tg_flMetalness "0.000"\n')

    # Ajoute les paramètres par défaut
    for param, value in default_parameters.items():
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
            process_texture_folder(folder_path, texture_mapping)

if __name__ == "__main__":
    main()
