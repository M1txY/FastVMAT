import os
import shutil
import subprocess
from PIL import Image
from config import TEXTURE_MAPPING, DEFAULT_PARAMETERS

def convert_dss_to_png(source_path, target_path):
    """
    Converts a .dss file to .png.
    """
    try:
        # Placeholder: Pillow may not support .dss directly. 
        # Replace with appropriate conversion logic or tool if needed.
        with Image.open(source_path) as img:
            img.save(target_path, format="PNG")
        print(f"Converted {source_path} to {target_path}")
    except Exception as e:
        print(f"Error converting {source_path}: {e}")

def process_dss_files(source_folder, target_folder):
    """
    Processes and converts all .dss files in a folder to .png.
    """
    for file in os.listdir(source_folder):
        if file.endswith(".dss"):
            source_path = os.path.join(source_folder, file)
            target_path = os.path.join(target_folder, file.replace(".dss", ".png"))
            convert_dss_to_png(source_path, target_path)
            os.remove(source_path)  # Cleanup the original .dss file

def split_channels(image_path, target_folder):
    """
    Splits the RGB channels of an image and saves them separately.
    """
    try:
        with Image.open(image_path) as img:
            channels = ['Metalness', 'Roughness', 'AO']
            paths = {}
            
            for channel, color in zip(channels, img.split()):
                file_name = f"{os.path.splitext(os.path.basename(image_path))[0]}_{channel}.png"
                channel_path = os.path.join(target_folder, file_name)
                color.save(channel_path)
                paths[channel] = channel_path

            os.remove(image_path)  # Remove the original file
            return paths
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def extract_textures(umodel_path, folder_path):
    """
    Extracts textures from .uasset files in a folder.
    """
    for file in os.listdir(folder_path):
        if file.endswith(".uasset"):
            file_path = os.path.join(folder_path, file)
            subprocess.run([umodel_path, "-export", file_path], cwd=folder_path, check=True)
            
            export_folder = os.path.join(folder_path, "UmodelExport")
            if os.path.exists(export_folder):
                process_dss_files(export_folder, folder_path) 
                convert_textures(export_folder, folder_path)
                shutil.rmtree(export_folder) 
            os.remove(file_path) 

def convert_textures(source_folder, target_folder):
    """
    Converts .tga files in the source folder to .png in the target folder.
    """
    for file in os.listdir(source_folder):
        if file.endswith(".tga"):
            source_path = os.path.join(source_folder, file)
            target_path = os.path.join(target_folder, file.replace(".tga", ".png"))
            try:
                with Image.open(source_path) as img:
                    img.save(target_path, format="PNG")
            except Exception as e:
                print(f"Error converting {source_path}: {e}")

def find_and_process_mra(folder_path):
    """
    Searches for and processes MRA textures in a folder.
    """
    for file in os.listdir(folder_path):
        if "mra" in file.lower() and file.endswith((".png", ".jpg", ".jpeg", ".tga")):
            file_path = os.path.join(folder_path, file)
            return split_channels(file_path, folder_path)
    return {}

def assign_textures(folder_path):
    """
    Assigns textures to their corresponding keys based on naming conventions.
    """
    textures = {}
    for file in os.listdir(folder_path):
        if file.endswith((".png", ".jpg", ".jpeg", ".tga")):
            for key, suffixes in TEXTURE_MAPPING.items():
                if any(suffix in file.lower() for suffix in suffixes):
                    textures[key] = os.path.relpath(os.path.join(folder_path, file), "materials").replace("\\", "/")
                    break
    return textures

def generate_vmat(folder_path, textures, options):
    """
    Generates a .vmat file using the provided textures and options.
    """
    base_name = os.path.basename(folder_path)
    vmat_path = os.path.join(folder_path, f"{base_name}.vmat")
    
    with open(vmat_path, "w") as vmat_file:
        vmat_file.write("// THIS FILE IS AUTO-GENERATED\n")
        vmat_file.write("Layer0\n{\n")
        vmat_file.write(f'\tshader "{DEFAULT_PARAMETERS["shader"]}"\n')
        
        for option, enabled in options.items():
            if enabled:
                vmat_file.write(f"\t{option} 1\n")
        if not options["F_METALNESS_TEXTURE"]:
            vmat_file.write('\tg_flMetalness "0.000"\n')

        for param, value in DEFAULT_PARAMETERS.items():
            vmat_file.write(f'\t{param} "{value}"\n')
        
        for key, path in textures.items():
            vmat_file.write(f'\t{key} "{path}"\n')
        
        vmat_file.write("}\n")
    
    print(f"Generated: {vmat_path}")

def process_folder(folder_path, umodel_path):
    """
    Processes a single folder to extract textures and generate a .vmat file.
    """
    extract_textures(umodel_path, folder_path)
    options = {
        "F_SPECULAR": False,
        "F_SELF_ILLUM": False,
        "F_METALNESS_TEXTURE": False,
    }
    
    mra_textures = find_and_process_mra(folder_path)
    if mra_textures:
        options["F_METALNESS_TEXTURE"] = True
    
    textures = assign_textures(folder_path)
    textures.update(mra_textures)

    generate_vmat(folder_path, textures, options)

def main():
    root_folder = "materials"
    umodel_path = os.path.abspath("umodel_64.exe")
    
    if not os.path.exists(root_folder):
        print(f"Root folder '{root_folder}' not found.")
        return

    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            process_folder(folder_path, umodel_path)

if __name__ == "__main__":
    main()
