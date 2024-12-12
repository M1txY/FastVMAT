# FastVMAT

**FastVMAT** est un outil Python avancé conçu pour simplifier et accélérer l'importation de nombreux matériaux dans **S&box** en générant automatiquement des fichiers `.vmat` compatibles avec le moteur **Source 2**. Il analyse vos textures organisées dans des sous-dossiers et crée les fichiers nécessaires en utilisant des configurations personnalisables. De plus, il intègre des fonctionnalités avancées telles que la séparation des canaux MRA et l'extraction des textures depuis les fichiers `.uasset`.

---

## Fonctionnalités

- 🚀 **Génération rapide** : Crée automatiquement des fichiers `.vmat` pour chaque sous-dossier contenant des textures.
- 🔍 **Détection par suffixes** : Analyse les noms des textures pour les mapper aux paramètres correspondants (albedo, normal, roughness, etc.).
- ⚙️ **Personnalisation facile** : Configurez les suffixes et les paramètres via un fichier `config.py`.
- 🌟 **Compatibilité Source 2** : Adapté aux besoins des projets S&box et autres jeux utilisant Source 2.
- 🔄 **Conversion automatique DDS et TGA en PNG** : Détecte et convertit les fichiers `.dds`, `.dss` ou `.tga` en `.png` avant traitement.
- 🎨 **Séparation des canaux MRA** : Sépare les canaux R, G et B des textures MRA en fichiers PNG distincts pour Metalness, Roughness et AO.
- 🛠️ **Extraction des textures depuis les fichiers `.uasset`** : Utilise **Umodel** pour extraire les textures des fichiers `.uasset` et les convertir en `.png`.

---

## Prérequis

1. **Python 3.x** installé sur votre système.
2. Une structure de dossiers organisée sous un dossier `materials` :
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
3. Un fichier de configuration `config.py` pour personnaliser les suffixes et les paramètres par défaut.

---

## Installation

1. Clonez ou téléchargez ce projet dans votre répertoire de travail :
    ```bash
    git clone https://github.com/M1txY/FastVMAT.git
    cd FastVMAT
    ```

2. Installez Python si ce n'est pas déjà fait :
    - [Téléchargez Python ici](https://www.python.org/downloads/).

3. Installez les dépendances nécessaires via `requirements.txt` :
    ```bash
    pip install -r requirements.txt
    ```

4. Assurez-vous que **Umodel** (`umodel_64.exe` pour Windows ou la version appropriée pour votre système) est placé dans le répertoire racine du projet ou ajustez le chemin dans le script si nécessaire.

---

## Configuration

1. **config.py** : Personnalisez les mappings des textures et les paramètres par défaut en modifiant le fichier `config.py`. Exemple :
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

## Utilisation

1. **Préparation des textures** :
    - Placez vos textures dans des sous-dossiers sous `materials/`. Chaque sous-dossier doit contenir les textures pour un matériau unique.
    - Exemple de structure :
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

2. **Extraction des textures depuis les fichiers `.uasset`** (si applicable) :
    - Assurez-vous que vos fichiers `.uasset` sont placés dans les dossiers appropriés sous `materials/`.
    - **Umodel** sera utilisé pour extraire les textures lors de l'exécution du script.

3. **Exécution du script Python** :
    ```bash
    python script.py
    ```

4. **Ce que fait le script** :
    - Analyse chaque sous-dossier dans `materials`.
    - Identifie les textures en fonction de leurs suffixes définis dans `config.py`.
    - Convertit les fichiers `.dds`, `.dss` ou `.tga` en `.png` si nécessaire.
    - Sépare les canaux R, G et B des textures MRA en fichiers PNG distincts pour Metalness, Roughness et AO.
    - Extrait les textures des fichiers `.uasset` en utilisant **Umodel**.
    - Génère un fichier `.vmat` pour chaque sous-dossier avec les paramètres et les chemins des textures appropriés.

5. **Résultat** :
    - Pour chaque sous-dossier de `materials/`, un fichier `.vmat` sera généré contenant les références aux textures traitées.

---

## Dépendances

Ce projet utilise les bibliothèques suivantes :

- **Pillow** : Pour le traitement des images.
- **Umodel** : Pour l'extraction des textures depuis les fichiers `.uasset`.

Vous pouvez installer les dépendances Python à l'aide du fichier `requirements.txt` :
```bash
pip install -r requirements.txt
```

### Contenu de `requirements.txt` :
```
Pillow
```

---

## Exemple de Résultat

### Structure initiale

```
materials/
├── wood_material/
│   ├── wood_albedo.dds
│   ├── wood_normal.dds
│   ├── wood_roughness.dds
```

### Résultat après exécution

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

### Contenu du fichier `.vmat`

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

### Mes textures ne sont pas détectées. Pourquoi ?

- **Vérifiez les suffixes** : Assurez-vous que les noms de fichiers contiennent les suffixes définis dans `TEXTURE_MAPPING` de `config.py`.
- **Extensions reconnues** : Assurez-vous que vos fichiers ont des extensions reconnues (`.png`, `.jpg`, `.jpeg`, `.tga`, `.dds`, `.dss`).
- **Structure des dossiers** : Vérifiez que vos textures sont placées dans des sous-dossiers corrects sous `materials/`.

### Puis-je utiliser ce script pour d'autres jeux Source 2 ?

- **Oui**, tant que vous respectez les structures de fichiers et les shaders compatibles avec Source 2.

### Comment personnaliser les paramètres par défaut ?

- **Modifiez `config.py`** : Ajustez les mappings des textures et les paramètres par défaut selon vos besoins dans le fichier `config.py`.

### Que faire si l'extraction des `.uasset` échoue ?

- **Vérifiez Umodel** : Assurez-vous que **Umodel** est correctement installé et accessible.
- **Compatibilité des fichiers** : Certains fichiers `.uasset` peuvent ne pas être compatibles avec **Umodel**. Vérifiez la documentation de **Umodel** pour plus de détails.

---

## Contribution

N'hésitez pas à proposer des améliorations ou à signaler des problèmes en ouvrant une [issue](https://github.com/M1txY/FastVMAT/issues) ou en soumettant une [pull request](https://github.com/M1txY/FastVMAT/pulls).

---

### Changements récents :

1. **Ajout de la séparation des canaux MRA** : Les textures MRA sont désormais séparées en Metalness, Roughness et AO.
2. **Extraction des textures depuis les fichiers `.uasset`** : Intégration de **Umodel** pour extraire et convertir automatiquement les textures.
3. **Conversion des fichiers TGA en PNG** : Ajout de la conversion automatique des fichiers `.tga` en `.png`.
4. **Mise à jour des instructions d'installation et d'utilisation** : Documentation améliorée pour refléter les nouvelles fonctionnalités.
