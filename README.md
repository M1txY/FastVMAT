# FastVMAT

**FastVMAT** is an advanced Python tool designed to simplify and accelerate the import of numerous materials into **S&box** by automatically generating `.vmat` files compatible with the **Source 2** engine. It analyzes your textures organized into subfolders and creates the necessary files using customizable configurations. Additionally, it integrates advanced features such as MRA channel separation and texture extraction from `.uasset` files.

---

## Features

- 🚀 **Fast Generation**: Automatically creates `.vmat` files for each subfolder containing textures.
- 🔍 **Suffix-Based Detection**: Analyzes texture names to map them to corresponding parameters (albedo, normal, roughness, etc.).
- ⚙️ **Easy Customization**: Configure suffixes and parameters via a `config.py` file.
- 🌟 **Source 2 Compatibility**: Tailored to the needs of S&box projects and other games using Source 2.
- 🔄 **Automatic DDS and TGA to PNG Conversion**: Detects and converts `.dds`, `.dss`, or `.tga` files to `.png` before processing.
- 🎨 **MRA Channel Separation**: Splits the R, G, and B channels of MRA textures into separate PNG files for Metalness, Roughness, and AO.
- 🛠️ **Texture Extraction from `.uasset` Files**: Uses **Umodel** to extract textures from `.uasset` files and convert them to `.png`.

---

## Prerequisites

1. **Python 3.x** installed on your system.
2. An organized folder structure under a `materials` directory:
    ```
    materials/
    ├── wood_material/
    │   ├── wood_albedo.png
    │   ├── wood_normal.png
    │   ├── wood_roughness.png
    ├── metal_material/
    │   ├── metal_albedo.tga
    │   ├── metal_metallic.tga
    │   ├── metal_normal.tga
    ├── glass_material/
    │   ├── glass_albedo.png
    │   ├── glass_translucency.png
    ```
3. A `config.py` configuration file to customize suffixes and default parameters.

---

## Installation

1. Clone or download this project to your working directory:
    ```bash
    git clone https://github.com/M1txY/FastVMAT.git
    cd FastVMAT
    ```

2. Install Python if it's not already installed:
    - [Download Python here](https://www.python.org/downloads/).

3. Install the necessary dependencies via `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure that **Umodel** (`umodel_64.exe` for Windows or the appropriate version for your system) is placed in the root directory of the project or adjust the path in the script if necessary.

---

## Configuration

1. **config.py**: Customize texture mappings and default parameters by modifying the `config.py` file. Example:
    ```python
    TEXTURE_MAPPING = {
        "TextureColor": ["albedo", "diffuse"],
        "TextureNormal": ["normal"],
        "TextureRoughness": ["roughness"],
        "TextureMetalness": ["metallic", "metalness"],
        "TextureAO": ["ao", "ambient_occlusion"],
        "TextureSelfIllumMask": ["self_illum", "emissive"]
    }

    DEFAULT_PARAMETERS = {
        "shader": "complex.shader",
        "g_flMetalness": "0.000",
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
        "g_vTexCoordScrollSpeed": "[0.000 0.000]"
    }
    ```

---

## Usage

1. **Prepare Textures**:
    - Place your textures in subfolders under `materials/`. Each subfolder should contain textures for a unique material.
    - Example structure:
        ```
        materials/
        ├── wood_material/
        │   ├── wood_albedo.png
        │   ├── wood_normal.png
        │   ├── wood_roughness.png
        ├── metal_material/
        │   ├── metal_albedo.tga
        │   ├── metal_metallic.tga
        │   ├── metal_normal.tga
        ├── glass_material/
        │   ├── glass_albedo.png
        │   ├── glass_translucency.png
        ```

2. **Extract Textures from `.uasset` Files** (if applicable):
    - Ensure that your `.uasset` files are placed in the appropriate folders under `materials/`.
    - **Umodel** will be used to extract textures during the script execution.

3. **Run the Python Script**:
    ```bash
    python script.py
    ```

4. **What the Script Does**:
    - Analyzes each subfolder in `materials`.
    - Identifies textures based on their suffixes defined in `config.py`.
    - Converts `.dds`, `.dss`, or `.tga` files to `.png` if necessary.
    - Splits the R, G, and B channels of MRA textures into separate PNG files for Metalness, Roughness, and AO.
    - Extracts textures from `.uasset` files using **Umodel**.
    - Generates a `.vmat` file for each subfolder with the appropriate parameters and texture paths.

5. **Result**:
    - For each subfolder in `materials/`, a `.vmat` file will be generated containing references to the processed textures.

---

## Dependencies

This project uses the following libraries:

- **Pillow**: For image processing.
- **Umodel**: For extracting textures from `.uasset` files.

You can install the Python dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Contents of `requirements.txt`:
```
Pillow
```

---

## Example Result

### Initial Structure

```
materials/
├── wood_material/
│   ├── wood_albedo.dds
│   ├── wood_normal.dds
│   ├── wood_roughness.dds
```

### Result After Execution

```
materials/
├── wood_material/
│   ├── wood_albedo.png
│   ├── wood_normal.png
│   ├── wood_roughness.png
│   ├── wood_Metalness.png
│   ├── wood_Roughness.png
│   ├── wood_AO.png
│   ├── wood_material.vmat
```

### Contents of the `.vmat` File

```plaintext
// THIS FILE IS AUTO-GENERATED

Layer0
{
    shader "complex.shader"

    //---- PBR ----
    F_SPECULAR 1
    F_SELF_ILLUM 0
    F_METALNESS_TEXTURE 1
    g_flMetalness "0.000"

    g_flAmbientOcclusionDirectDiffuse "0.000"
    g_flAmbientOcclusionDirectSpecular "0.000"
    g_flModelTintAmount "1.000"
    g_vColorTint "[1.000000 1.000000 1.000000 0.000000]"
    g_flFadeExponent "1.000"
    g_bFogEnabled "1"
    g_flRoughnessScaleFactor "1.000"
    g_nScaleTexCoordUByModelScaleAxis "0"
    g_nScaleTexCoordVByModelScaleAxis "0"
    g_vTexCoordOffset "[0.000 0.000]"
    g_vTexCoordScale "[1.000 1.000]"
    g_vTexCoordScrollSpeed "[0.000 0.000]"

    TextureMetalness "materials/wood_material/wood_Metalness.png"
    TextureRoughness "materials/wood_material/wood_Roughness.png"
    TextureAO "materials/wood_material/wood_AO.png"
    TextureColor "materials/wood_material/wood_albedo.png"
    TextureNormal "materials/wood_material/wood_normal.png"
    TextureRoughness "materials/wood_material/wood_roughness.png"
}
```

---

## FAQ

### My textures are not being detected. Why?

- **Check Suffixes**: Ensure that the filenames contain the suffixes defined in `TEXTURE_MAPPING` in `config.py`.
- **Recognized Extensions**: Make sure your files have recognized extensions (`.png`, `.jpg`, `.jpeg`, `.tga`, `.dds`, `.dss`).
- **Folder Structure**: Verify that your textures are placed in the correct subfolders under `materials/`.

### Can I use this script for other Source 2 games?

- **Yes**, as long as you adhere to the file structures and shaders compatible with Source 2.

### How can I customize the default parameters?

- **Modify `config.py`**: Adjust the texture mappings and default parameters as needed in the `config.py` file.

### What should I do if extracting `.uasset` files fails?

- **Check Umodel**: Ensure that **Umodel** is correctly installed and accessible.
- **File Compatibility**: Some `.uasset` files might not be compatible with **Umodel**. Check the **Umodel** documentation for more details.

---

## Contribution

Feel free to propose improvements or report issues by opening an [issue](https://github.com/M1txY/FastVMAT/issues) or submitting a [pull request](https://github.com/M1txY/FastVMAT/pulls).

---

### Recent Changes:

1. **Added MRA Channel Separation**: MRA textures are now split into Metalness, Roughness, and AO.
2. **Texture Extraction from `.uasset` Files**: Integrated **Umodel** to automatically extract and convert textures.
3. **TGA to PNG File Conversion**: Added automatic conversion of `.tga` files to `.png`.
4. **Updated Installation and Usage Instructions**: Improved documentation to reflect new features.