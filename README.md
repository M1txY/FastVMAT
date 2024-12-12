# FastVMAT

**FastVMAT** est un outil Python conçu pour simplifier et accélérer l'importation de nombreux matériaux dans **S&box** en générant automatiquement des fichiers `.vmat` compatibles avec le moteur **Source 2**. Il analyse vos textures organisées dans des sous-dossiers et crée les fichiers nécessaires en utilisant des configurations personnalisables.

---

## Fonctionnalités

- 🚀 **Génération rapide** : Crée automatiquement des fichiers `.vmat` pour chaque sous-dossier contenant des textures.
- 🔍 **Détection par suffixes** : Analyse les noms des textures pour les mapper aux paramètres correspondants (albedo, normal, roughness, etc.).
- ⚙️ **Personnalisation facile** : Configurez les suffixes et les paramètres via un fichier `config.py`.
- 🌟 **Compatibilité Source 2** : Adapté aux besoins des projets S&box et autres jeux utilisant Source 2.
- 🔄 **Conversion automatique DDS en PNG** : Détecte et convertit les fichiers `.dds` ou `.dss` en `.png` avant traitement.

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
   - Convertir les fichiers `.dds` ou `.dss` en `.png` si nécessaire.
   - Générer un fichier `.vmat` pour chaque sous-dossier.

---

## Dépendances

Ce projet utilise la bibliothèque **Pillow** pour le traitement des images. Vous pouvez installer cette dépendance et les autres nécessaires à l'aide du fichier `requirements.txt`.

### Installer les dépendances :
```bash
pip install -r requirements.txt
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
- Assurez-vous que vos fichiers ont des extensions reconnues (`.png`, `.jpg`, `.tga`, `.dds`, etc.).

### Puis-je utiliser ce script pour d'autres jeux Source 2 ?
- Oui, tant que vous respectez les structures de fichiers et les shaders compatibles avec Source 2.

---

## Contribution

N'hésitez pas à proposer des améliorations ou à signaler des problèmes en ouvrant une issue ou en soumettant une pull request.

---

### Changements :
1. **Section Dépendances** : Ajout d'instructions pour installer les dépendances avec `requirements.txt`.
2. **Conversion automatique DDS en PNG** : Mention explicite de la fonctionnalité dans la description et les étapes d'utilisation.

N'hésitez pas à demander des ajustements si nécessaire ! 😊