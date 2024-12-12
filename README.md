
# FastVMAT

**FastVMAT** est un outil Python conçu pour simplifier et accélérer l'importation de nombreux matériaux dans **S&box** en générant automatiquement des fichiers `.vmat` compatibles avec le moteur **Source 2**. Il analyse vos textures organisées dans des sous-dossiers et crée les fichiers nécessaires en utilisant des configurations personnalisables.

---

## Fonctionnalités

- 🚀 **Génération rapide** : Crée automatiquement des fichiers `.vmat` pour chaque sous-dossier contenant des textures.
- 🔍 **Détection par suffixes** : Analyse les noms des textures pour les mapper aux paramètres correspondants (albedo, normal, roughness, etc.).
- ⚙️ **Personnalisation facile** : Configurez les suffixes et les paramètres via un fichier `config.py`.
- 🌟 **Compatibilité Source 2** : Adapté aux besoins des projets S&box et autres jeux utilisant Source 2.

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

## Configuration

### Modifier les Suffixes

Le fichier `config.py` contient la configuration des suffixes utilisés pour détecter les textures. Voici un exemple de configuration par défaut :

```python
TEXTURE_MAPPING = {
    "TextureColor": ["_albedo", "_diffuse", "_basecolor", "_color", "_col", "_bc", "_diff"],
    "TextureAmbientOcclusion": ["_ao", "_ambientocclusion", "_occlusion", "_ambocc", "_aoc", "_occl"],
    "TextureNormal": ["_normal", "_nor", "_norm", "_nrm", "_normalmap", "_nml", "_bump"],
    "TextureRoughness": ["_roughness", "_rou", "_rgh", "_gloss", "_gls", "_rough", "_specular"],
    "TextureMetalness": ["_metallic", "_met", "_metal", "_mtl", "_metalness", "_metall"],
    "TextureSelfIllumMask": ["_selfillum", "_illum", "_glowmask", "_emit", "_emissive", "_light"],
    "TextureTranslucency": ["_translucent", "_trans", "_opacity", "_opa", "_alpha"]
}
```

Si vos textures utilisent des suffixes différents, modifiez-les dans `TEXTURE_MAPPING`. Par exemple :
```python
TEXTURE_MAPPING = {
    "TextureColor": ["_base"],
    "TextureNormal": ["_normmap"]
}
```

### Modifier les Paramètres par Défaut

Les paramètres par défaut pour les fichiers `.vmat` sont définis dans `config.py` :

```python
DEFAULT_PARAMETERS = {
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
    "g_vTexCoordScrollSpeed": "[0.000 0.000]"
}
```

---

## Installation

1. Clonez ou téléchargez ce projet dans votre répertoire de travail :
   ```bash
   git clone https://github.com/M1txY/FastVMAT.git
   cd FastVMAT
   ```

2. Installez Python si ce n'est pas déjà fait :
   - [Téléchargez Python ici](https://www.python.org/downloads/).


---

## Utilisation

1. Placez vos textures dans des sous-dossiers sous `materials/`. Chaque sous-dossier doit contenir les textures pour un matériau unique.

2. Exécutez le script Python :
   ```bash
   python script.py
   ```

3. Le script va :
   - Analyser chaque sous-dossier dans `materials`.
   - Identifier les textures en fonction de leurs suffixes.
   - Générer un fichier `.vmat` pour chaque sous-dossier.

---

## Exemple de Résultat

### Structure initiale

```
materials/
├── wood_material/
│   ├── wood_albedo.png
│   ├── wood_normal.png
│   ├── wood_roughness.png
```

### Résultat après exécution

```
materials/
├── wood_material/
│   ├── wood_albedo.png
│   ├── wood_normal.png
│   ├── wood_roughness.png
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

    TextureColor "materials/wood_material/wood_albedo.png"
    TextureNormal "materials/wood_material/wood_normal.png"
    TextureRoughness "materials/wood_material/wood_roughness.png"
}
```

---

## FAQ

### Mes textures ne sont pas détectées. Pourquoi ?
- Vérifiez que les noms de fichiers contiennent les suffixes définis dans `TEXTURE_MAPPING`.
- Assurez-vous que vos fichiers ont des extensions reconnues (`.png`, `.jpg`, `.tga`, etc.).

### Puis-je utiliser ce script pour d'autres jeux Source 2 ?
- Oui, tant que vous respectez les structures de fichiers et les shaders compatibles avec Source 2.

---

## Contribution

N'hésitez pas à proposer des améliorations ou à signaler des problèmes en ouvrant une issue ou en soumettant une pull request.

