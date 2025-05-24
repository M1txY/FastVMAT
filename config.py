
TEXTURE_MAPPING = {
    "TextureColor": ["_albedo", "_diffuse", "_basecolor", "_color", "_col", "_bc", "_diff", "_a"],
    "TextureAmbientOcclusion": ["_ao", "_ambientocclusion", "_occlusion", "_ambocc", "_aoc", "_occl"],
    "TextureNormal": ["_normal", "_nor", "_norm", "_nrm", "_normalmap", "_nml", "_bump", "_n"],
    "TextureRoughness": ["_roughness", "_rou", "_rgh", "_gloss", "_gls", "_rough", "_specular"],
    "TextureMetalness": ["_metallic", "_met", "_metal", "_mtl", "_metalness", "_metall"],
    "TextureSelfIllumMask": ["_selfillum", "_illum", "_glowmask", "_emit", "_emissive", "_light"],
    "TextureTranslucency": ["_translucent", "_trans", "_opacity", "_opa", "_alpha"]
}


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
