from pygltflib import GLTF2
import base64
from pathlib import Path
from PIL import Image
import io

def extract_textures(gltf_file, output_folder):
    # Charger le fichier GLTF
    gltf = GLTF2().load(gltf_file)

    # Créer le dossier de sortie
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    # Parcourir les images dans le GLTF
    if not gltf.images:
        print("Aucune texture trouvée dans le fichier GLTF.")
        return
    
    for idx, image in enumerate(gltf.images):
        # Gérer les images intégrées (base64) ou externes
        if image.uri:
            if image.uri.startswith("data:"):
                # Image encodée en base64
                data = image.uri.split(",")[1]
                img_data = base64.b64decode(data)
                img = Image.open(io.BytesIO(img_data))
                img.save(output_folder / f"texture_{idx}.png")
                print(f"Texture {idx} extraite et sauvegardée : texture_{idx}.png")
            else:
                # Image externe
                print(f"Texture {idx} déjà externe : {image.uri}")
        elif gltf.buffers and gltf.bufferViews:
            # Gérer les textures stockées dans les buffers binaires
            buffer_view = gltf.bufferViews[image.bufferView]
            buffer = gltf.buffers[buffer_view.buffer]
            binary_data = buffer.data[buffer_view.byteOffset:buffer_view.byteOffset + buffer_view.byteLength]
            img = Image.open(io.BytesIO(binary_data))
            img.save(output_folder / f"texture_{idx}.png")
            print(f"Texture {idx} extraite depuis le buffer et sauvegardée : texture_{idx}.png")
        else:
            print(f"Impossible de traiter la texture {idx}")

# Exemple d'utilisation
gltf_file = "model.gltf"  # Remplacez par le chemin de votre fichier GLTF
output_folder = "textures_output"  # Dossier où sauvegarder les PNG
extract_textures(gltf_file, output_folder)