# === CLASSIC VALUES (from your earlier table) ===
from dashboard.acsos_vars import ACSOS_STD_DEV, ACSOS_DATASET_NAMES, ACSOS_MEANS

CLASSIC_CGP_DATASET_NAMES = [
    "FabricDefectsAITEX",
    "KolektorSDD",
    "MVTec_AD_Bottle_Broken_Lg",
    "MVTec_AD_Bottle_Broken_Sm",
    "MVTec_AD_Cable_Missing",
    "MVTec_AD_Capsule",
    "MVTec_AD_Carpet",
    "MVTec_AD_Grid_Thread",
    "MVTec_AD_Hazelnut_Crack",
    "MVTec_D_Leather",
    "MVTec_AD_Metal_Nut",
    "MVTec_AD_Pill_Crack",
    "MVTec_AD_Screw_Scratch",
    "MVTec_AD_Tile_Crack",
    "MVTec_AD_Wood_Scratch",
    "MVTec_AD_Zipper_Rough",
    "Pultrusion_Resin",
    "Pultrusion_Resin_Augmtd",
    "Pultrusion_Window",
    "severstal-steel"
]

CLASSIC_CGP_MEANS = [
    0.151, 0.057, 0.323, 0.235, 0.505, 0.141, 0.116, 0.275, 0.429,
    0.336, 0.121, 0.326, 0.164, 0.504, 0.355, 0.433, 0.612, 0.376, 0.654, 0.183
]

CLASSIC_CGP_STD_DEV = [
    0.025, 0.031, 0.024, 0.080, 0.146, 0.056, 0.041, 0.189, 0.091,
    0.119, 0.015, 0.219, 0.061, 0.214, 0.175, 0.134, 0.128, 0.109, 0.040, 0.073
]

# Mapping from CLASSIC dataset names to ACSOS equivalents
ACSOS_CLASSIC_MAP = {
    "FabricDefectsAITEX": "FabricDefects",
    "KolektorSDD": "KolektorSDD",
    "MVTec_AD_Bottle_Broken_Lg": "Bottle_Brkn_Lg",
    "MVTec_AD_Bottle_Broken_Sm": "Bottle_Brkn_Sm",
    "MVTec_AD_Cable_Missing": "Cable_Missing",
    "MVTec_AD_Capsule": "Capsule",
    "MVTec_AD_Carpet": "Carpet",
    "MVTec_AD_Grid_Thread": "Grid_Thread",
    "MVTec_AD_Hazelnut_Crack": "Hazelnut_Crack",
    "MVTec_D_Leather": "Leather",
    "MVTec_AD_Metal_Nut": "Metal_Nut",
    "MVTec_AD_Pill_Crack": "Pill_Crack",
    "MVTec_AD_Screw_Scratch": "Screw_Scratch",
    "MVTec_AD_Tile_Crack": "Tile_Crack",
    "MVTec_AD_Wood_Scratch": "Wood_Scratch",
    "MVTec_AD_Zipper_Rough": "Zipper_Rough",
    "Pultrusion_Resin": "Pul_Resin",
    "Pultrusion_Resin_Augmtd": "Pul_Resin_Augtd",
    "Pultrusion_Window": "Pul_Window",
    "severstal-steel": "severstal-steel"
}

def get_harmonized_values():
    reduced_acsos_mean = []
    reduced_acsos_std_dev = []
    reduced_acsos_dataset_names = []

    for classic_name in CLASSIC_CGP_DATASET_NAMES:
        try:
            idx, acsos_mean, acsos_std = get_acsos_values(classic_name)
            reduced_acsos_mean.append(ACSOS_MEANS[idx])
            reduced_acsos_std_dev.append(ACSOS_STD_DEV[idx])
            reduced_acsos_dataset_names.append(ACSOS_DATASET_NAMES[idx])
        except ValueError as e:
            print(e)

    if len(reduced_acsos_mean) != len(CLASSIC_CGP_MEANS) or len(reduced_acsos_std_dev) != len(CLASSIC_CGP_STD_DEV):
        raise ValueError("Mismatch in dataset lengths after harmonization.")

    return reduced_acsos_mean, reduced_acsos_std_dev, reduced_acsos_dataset_names


def get_acsos_values(classic_name):
    """
    Given a CLASSIC dataset name, look up its ACSOS equivalent,
    return (index, mean, stddev) from the ACSOS lists.
    """
    if classic_name not in ACSOS_CLASSIC_MAP:
        raise ValueError(f"No ACSOS mapping found for {classic_name}")

    acsos_name = ACSOS_CLASSIC_MAP[classic_name]
    try:
        idx = ACSOS_DATASET_NAMES.index(acsos_name)
    except ValueError:
        raise ValueError(f"{acsos_name} not found in ACSOS_DATASET_NAMES")

    return idx, ACSOS_MEANS[idx], ACSOS_STD_DEV[idx]

# Example usage:
# idx, mean, std = get_acsos_values("Pultrusion_Window", ACSOS_DATASET_NAMES, ACSOS_MEANS, ACSOS_STD_DEV)
# print(idx, mean, std)