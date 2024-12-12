import os
import shutil
import subprocess
from PIL import Image
from config import TEXTURE_MAPPING, DEFAULT_PARAMETERS

def split_mra_texture(mra_path, target_folder):
    """
    Splits the R, G, and B channels of an MRA texture into separate PNG files
    and returns their paths for updating in the texture dictionary.
    """
    if not os.path.exists(mra_path):
        print(f"MRA file not found: {mra_path}")
        return None, None, None

    try:
        print(f"Attempting to split: {mra_path}")
        with Image.open(mra_path) as img:
            r, g, b = img.split()
            
            base_name = os.path.basename(mra_path).replace(".png", "")
            base_name = base_name[:-4]
            r_path = os.path.join(target_folder, f"{base_name}_Metalness.png")
            g_path = os.path.join(target_folder, f"{base_name}_Roughness.png")
            b_path = os.path.join(target_folder, f"{base_name}_AO.png")
            
            r.save(r_path)
            g.save(g_path)
            b.save(b_path)

            print(f"Channels successfully split: {r_path}, {g_path}, {b_path}")
            
            os.remove(mra_path)
            print(f"Original file deleted: {mra_path}")

            return r_path, g_path, b_path
    except Exception as e:
        print(f"Error splitting MRA channels: {e}")
        return None, None, None

def extract_uasset_to_png(umodel_path, folder_path):
    """
    Extracts textures from .uasset files and replaces the files with .png files.
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
                print(f"Extracting textures from: {file_name}")
                subprocess.run(command, check=True, cwd=folder_path)
                print(f"Textures extracted for: {file_name}")
                
                export_folder = os.path.join(folder_path, "UmodelExport")
                if os.path.exists(export_folder):
                    convert_and_move_tga_to_png(export_folder, folder_path)
                    shutil.rmtree(export_folder) 
                    print(f"Deleted: {export_folder}")
                
                if os.path.exists(input_path):
                    os.remove(input_path)
                    print(f"Deleted: {file_name}")

            except subprocess.CalledProcessError as e:
                print(f"Error extracting for {file_name}: {e}")

def convert_and_move_tga_to_png(source_folder, target_folder):
    """
    Converts .tga files to .png and moves them to the target folder.
    """
    for file_name in os.listdir(source_folder):
        if file_name.endswith(".tga"):
            tga_path = os.path.join(source_folder, file_name)
            png_path = os.path.join(target_folder, file_name.replace(".tga", ".png"))
            try:
                with Image.open(tga_path) as img:
                    img.save(png_path, format="PNG")
                    print(f"Converted and moved: {tga_path} -> {png_path}")
            except Exception as e:
                print(f"Error converting {tga_path}: {e}")

def process_texture_folder(folder_path):
    """
    Processes a folder to generate a .vmat file from the textures.
    """
    textures = {}
    base_name = os.path.basename(folder_path)
    
    options = {
        "F_SPECULAR": False,
        "F_SELF_ILLUM": False,
        "F_METALNESS_TEXTURE": False,
    }
    
    umodel_path = os.path.abspath("umodel_64.exe")
    extract_uasset_to_png(umodel_path, folder_path)
    
    mra_texture = None
    for file in os.listdir(folder_path):
        if "mra" in file.lower() and file.endswith((".png", ".jpg", ".jpeg", ".tga")):
            mra_texture = os.path.join(folder_path, file)
            break

    if mra_texture:
        print(f"MRA texture detected: {mra_texture}")
        r_path, g_path, b_path = split_mra_texture(mra_texture, folder_path)
        if r_path and g_path and b_path:
            textures["TextureMetalness"] = os.path.relpath(r_path, "materials").replace("\\", "/")
            textures["TextureRoughness"] = os.path.relpath(g_path, "materials").replace("\\", "/")
            textures["TextureAmbientOcclusion"] = os.path.relpath(b_path, "materials").replace("\\", "/")
            
            options["F_METALNESS_TEXTURE"] = True
            print("MRA textures replaced with Metalness, Roughness, and AO.")
        else:
            print("Failed to replace MRA texture.")
    
    for file in os.listdir(folder_path):
        if file.endswith((".png", ".jpg", ".jpeg", ".tga")):
            texture_relative_path = os.path.relpath(os.path.join(folder_path, file), "materials").replace("\\", "/")
            if texture_relative_path in textures.values():
                continue

            assigned = False
            for texture_key, suffix_list in TEXTURE_MAPPING.items():
                if any(suffix in file.lower() for suffix in suffix_list):
                    if texture_key == "TextureColor" and any(suffix in file.lower() for suffix in TEXTURE_MAPPING["TextureAmbientOcclusion"]):
                        print(f"Ignored: {file} detected as AO, not Base Color.")
                        continue
                    if textures.get(texture_key):
                        print(f"Warning: A texture is already assigned for {texture_key}.")
                        continue
                    relative_path = os.path.join(
                        "materials",
                        os.path.relpath(folder_path, "materials"),
                        file
                    ).replace("\\", "/")
                    textures[texture_key] = relative_path
                    assigned = True
                    # Enable options based on the detected texture
                    if texture_key == "TextureSelfIllumMask":
                        options["F_SELF_ILLUM"] = True
                    if texture_key == "TextureMetalness":
                        options["F_METALNESS_TEXTURE"] = True
                    if texture_key == "TextureSpecular":
                        options["F_SPECULAR"] = True
                    break
            if not assigned:
                print(f"No match found for: {file}")
    
    vmat_content = ["// THIS FILE IS AUTO-GENERATED\n", "Layer0\n{\n"]
    vmat_content.append(f'\tshader "{DEFAULT_PARAMETERS["shader"]}"\n\n')
    
    for option, enabled in options.items():
        if enabled:
            vmat_content.append(f"\t{option} 1\n")
    if not options["F_METALNESS_TEXTURE"]:
        vmat_content.append('\tg_flMetalness "0.000"\n')
    
    for param, value in DEFAULT_PARAMETERS.items():
        vmat_content.append(f'\t{param} "{value}"\n')
    
    for texture_key, texture_path in textures.items():
        vmat_content.append(f'\t{texture_key} "{texture_path}"\n')

    vmat_content.append("}\n")
    
    vmat_file_path = os.path.join(folder_path, f"{base_name}.vmat")
    with open(vmat_file_path, "w") as vmat_file:
        vmat_file.writelines(vmat_content)
    print(f"Generated: {vmat_file_path}")

def main():
    root_folder = "materials"
    if not os.path.exists(root_folder):
        print(f"The folder '{root_folder}' was not found.")
        return

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            process_texture_folder(folder_path)

if __name__ == "__main__":
    main()
