"""
DATASETS for Experiments
"""

aircarbon3_datasets = {
    '80.jpg_dark_1': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_1',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_2',
        'publisher': 'Fraunhofer'
    },
    '80.jpg_dark_2': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_2',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_3',
        'publisher': 'Fraunhofer'
    },
    '80.jpg_dark_3': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_3',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_4',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_3',
    '80.jpg_dark_4': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_4',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_5',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_4',
    '80.jpg_dark_5': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_5',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_1',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon3\\20210325_13h25_rov\\training\\80.jpg_dark_5',
}

aircarbon3_datasets_v2 = {
    '81.jpg_bright': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\81.jpg_bright',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\81.jpg',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon3\\20210325_13h25_rov\\training\\81.jpg_bright',
    '81.jpg_dark': {
        'train': 'Aircarbon3\\20210325_13h25_rov\\training\\81.jpg_dark',
        'test': 'Aircarbon3\\20210325_13h25_rov\\training\\81.jpg',
        'publisher': 'Fraunhofer'
    }  # 'Aircarbon3\\20210325_13h25_rov\\training\\81.jpg_dark'
}

aircarbon2_datasets = {
    't_8': {
        'train': 'Aircarbon2\\Blende5_6_1800mA_rov\\training\\t_8.jpg',
        'test': 'Aircarbon2\\Blende5_6_1800mA_rov\\training\\t_12.jpg',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon2\Blende5_6_1800mA_rov\\training\\t_8.jpg',
    'CF_RefSet': {
        'train': 'Aircarbon2\\CF_ReferenceSet',
        'test': 'Aircarbon2\\CF_ReferenceSet_Small_Light',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon2\\CF_ReferenceSet',
    'CF_RefSet_Small_Light': {
        'train': 'Aircarbon2\\CF_ReferenceSet_Small_Light',
        'test': 'Aircarbon2\\CF_ReferenceSet',
        'publisher': 'Fraunhofer'
    },  # 'Aircarbon2\\CF_ReferenceSet_Small_Light',
    'CF_ReferenceSet_Small_Dark': {
        'train': 'Aircarbon2\\CF_ReferenceSet_Small_Dark',
        'test': 'Aircarbon2\\CF_ReferenceSet',
        'publisher': 'Fraunhofer'
    }  # 'Aircarbon2\\CF_ReferenceSet_Small_Dark'
}

severstal_plain = {
    'severstal': {
        'train': 'severstal-steel\\train_cgp',
        'test': 'severstal-steel\\val_cgp',
        'publisher': 'Severstal'
    },  # 'severstal-steel\\train_cgp',
}

severstal_128 = {
    'severstal': {
        'train': 'severstal-steel\\train_cgp_square',
        'test': 'severstal-steel\\val_cgp_square',
        'publisher': 'Severstal'
    }
}

metal_datasets = {
    'MT_Blowhole_train': {
        'train': 'Magnetic-Tile-Defect\\MT_Blowhole_train',
        'test': 'Magnetic-Tile-Defect\\MT_Blowhole_val',
        'publisher': 'MT'
    },  # 'Magnetic-Tile-Defect\MT_Blowhole_train',
    'kos10': {
        'train': 'KolektorSDD\\kos10',
        'test': 'KolektorSDD\\kos25',
        'publisher': 'Kolektor'
    },  # 'KolektorSDD\\kos10',
    'kos25': {
        'train': 'KolektorSDD\\kos25',
        'test': 'KolektorSDD\\kos10',
        'publisher': 'Kolektor'
    },  # 'KolektorSDD\\kos25'
}

pultrusion_datasets = {
    'resin_cgp': {
        'train': 'Pultrusion\\resin_cgp\\train',
        'test': 'Pultrusion\\resin_cgp\\val',
        'publisher': 'Fraunhofer'
    },  # 'Pultrusion\\resin_cgp\\train',
    'window_cgp': {
        'train': 'Pultrusion\\window_cgp\\train',
        'test': 'Pultrusion\\window_cgp\\val',
        'publisher': 'Fraunhofer'
    },  # 'Pultrusion\\window_cgp\\train',
    'resin_cgp_augmented': {
        'train': 'Pultrusion\\resin_cgp_augmntd\\train',
        'test': 'Pultrusion\\resin_cgp_augmntd\\val',
        'publisher': 'Fraunhofer'
    },  # 'Pultrusion\\resin_cgp_augmntd\\train'
}

textile_datasets = {
    'FabricDefectsAITEX': {
        'train': 'FabricDefectsAITEX\\train',
        'test': 'FabricDefectsAITEX\\val',
        'publisher': 'AITEX'
    },  # 'FabricDefectsAITEX\\train'
}

mvtec_datasets = {
    'carpet': {
        'train': 'MVTecAnomalyDetection\\carpet_train',
        'test': 'MVTecAnomalyDetection\\carpet_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\carpet_train',
    'leather': {
        'train': 'MVTecAnomalyDetection\\leather_train',
        'test': 'MVTecAnomalyDetection\\leather_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\leather_train',
    'capsule': {
        'train': 'MVTecAnomalyDetection\\capsule_crack_train',
        'test': 'MVTecAnomalyDetection\\capsule_crack_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\capsule_crack_train',
    'metal_nut': {
        'train': 'MVTecAnomalyDetection\\metal_nut_color_train',
        'test': 'MVTecAnomalyDetection\\metal_nut_color_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\capsule_crack_train',
    'pill': {
        'train': 'MVTecAnomalyDetection\\pill_crack_train',
        'test': 'MVTecAnomalyDetection\\pill_crack_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\pill_crack_train',
    'grid_thread': {
        'train': 'MVTecAnomalyDetection\\grid_thread_train',
        'test': 'MVTecAnomalyDetection\\grid_thread_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\grid_thread_train',
    'toothbrush_small': {
        'train': 'MVTecAnomalyDetection\\toothbrush_small_train',
        'test': 'MVTecAnomalyDetection\\toothbrush_small_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\toothbrush_small_train',
    'tile_crack': {
        'train': 'MVTecAnomalyDetection\\tile_crack_train',
        'test': 'MVTecAnomalyDetection\\tile_crack_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\tile_crack_train',
    'wood_scratch': {
        'train': 'MVTecAnomalyDetection\\wood_scratch_train',
        'test': 'MVTecAnomalyDetection\\wood_scratch_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\wood_scratch_train',
    'zipper': {
        'train': 'MVTecAnomalyDetection\\zipper_rough_train',
        'test': 'MVTecAnomalyDetection\\zipper_rough_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\zipper_rough_train',
    'bottle_large': {
        'train': 'MVTecAnomalyDetection\\bottle_broken_large_train',
        'test': 'MVTecAnomalyDetection\\bottle_broken_large_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\bottle_broken_large_train',
    'bottle_small': {
        'train': 'MVTecAnomalyDetection\\bottle_broken_small_train',
        'test': 'MVTecAnomalyDetection\\bottle_broken_small_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\bottle_broken_small_train',
    'cable_missing_train': {
        'train': 'MVTecAnomalyDetection\\cable_missing_train',
        'test': 'MVTecAnomalyDetection\\cable_missing_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\cable_missing_train',
    'hazelnut_crack_train': {
        'train': 'MVTecAnomalyDetection\\hazelnut_crack_train',
        'test': 'MVTecAnomalyDetection\\hazelnut_crack_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\hazelnut_crack_train',
    'screw_scratch_neck_train': {
        'train': 'MVTecAnomalyDetection\\screw_scratch_neck_train',
        'test': 'MVTecAnomalyDetection\\screw_scratch_neck_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\screw_scratch_neck_train',
    'transistor_damaged_case_train': {
        'train': 'MVTecAnomalyDetection\\transistor_damaged_case_train',
        'test': 'MVTecAnomalyDetection\\transistor_damaged_case_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\transistor_damaged_case_train'
}

mvtec_toothbrush = {
    'toothbrush_small': {
        'train': 'MVTecAnomalyDetection\\toothbrush_small_train',
        'test': 'MVTecAnomalyDetection\\toothbrush_small_val',
        'publisher': 'MVTec AD'
    }  # 'MVTecAnomalyDetection\\toothbrush_small_train',
}

mvtec_tile_dataset = {
    'tile_crack': {
        'train': 'MVTecAnomalyDetection\\tile_crack_train',
        'test': 'MVTecAnomalyDetection\\tile_crack_val',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\tile_crack_train',
}

mvtec_tile_dataset_128 = {
    'tile_crack': {
        'train': 'MVTecAnomalyDetection\\tile_crack_train_square',
        'test': 'MVTecAnomalyDetection\\tile_crack_val_square',
        'publisher': 'MVTec AD'
    },  # 'MVTecAnomalyDetection\\tile_crack_train',
}

mvtec_cable_dataset = {
    'cable_missing_train': {
        'train': 'MVTecAnomalyDetection\\cable_missing_train',
        'test': 'MVTecAnomalyDetection\\cable_missing_val',
        'publisher': 'MVTec AD'
    }
}

mvtec_cable_dataset_128 = {
    'cable_missing_train': {
        'train': 'MVTecAnomalyDetection\\cable_missing_train_square',
        'test': 'MVTecAnomalyDetection\\cable_missing_val_square',
        'publisher': 'MVTec AD'
    }
}

# MaiPreform Roving with Gap
maipreform_datasets = {
    'spule-upside-0117': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule1_01117_Upside\\undone\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule1_0117_Upside\\undone\\training',
    'spule2-0816_Upside-dl1': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf1\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf2\\training',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf2\\training',
    'spule2-0816_Upside-dl2': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf2\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf1\\training',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf1\\training',
    'spule-upside-hole': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole\\training',
    'spule-upside-hole256': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training'
    'spule-upside-0315': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule1_01117_Upside\\undone\\training',
        'publisher': 'Fraunhofer'
    }  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training',
}

# reduced maipreform with only 5 images per dataset
maipreform_datasets_reduced = {
    'spule-upside-0117-reduced': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule1_01117_Upside\\undone\\training_small_subset',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training_small_subset',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule1_0117_Upside\\undone\\training',
    'spule2-0816_Upside-dl1-reduced': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf1\\training_small_subset',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf2\\training_small_subset',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf2\\training',
    'spule2-0816_Upside-dl2-reduced': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf2\\training_small_subset',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf1\\training_small_subset',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule2-0816_Upside\\undone\\durchlauf1\\training',
    'spule-upside-hole-reduced': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole\\training_small_subset',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training_small_subset',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole\\training',
    'spule-upside-hole256-reduced': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training_small_subset',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training_small_subset',
        'publisher': 'Fraunhofer'
    },  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone_thread_hole_256\\training'
    'spule-upside-0315': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training_small_subset',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule1_01117_Upside\\undone\\training_small_subset',
        'publisher': 'Fraunhofer'
    }  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training',
}

spule_upside_0315 = {
    'spule-upside-0315': {
        'train': 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training',
        'test': 'MAIPreform2.0\\20170502_Compositence\\Spule1_01117_Upside\\undone\\training',
        'publisher': 'Fraunhofer'
    }  # 'MAIPreform2.0\\20170502_Compositence\\Spule0-0315_Upside\\undone\\training',
}
# for use
cracks_datasets = {
    # 'bridge_crack_dataset': {
    #    'train': 'bridge_crack_dataset\\crack_segmentation_dataset',
    #    'test': 'bridge_crack_dataset\\crack_segmentation_dataset',
    # },
    'crack_forest': {
        'train': 'CrackForest',
        'test': 'CrackForest',
        'publisher': 'Chinese Academy of Sciences'
    }
}

cracks_datasets_reduced = {
    # 'bridge_crack_dataset': {
    #    'train': 'bridge_crack_dataset\\crack_segmentation_dataset',
    #    'test': 'bridge_crack_dataset\\crack_segmentation_dataset',
    # },
    'crack_forest': {
        'train': 'CrackForest\\small_dataset',
        'test': 'CrackForest\\small_dataset',
        'publisher': 'Chinese Academy of Sciences'
    }
}

DATASETS = {
    # **mvtec_tile_dataset_128, # resized to fit 128x128 size for augmented u-net
    # **mvtec_cable_dataset_128, # resized to fit 128x128 size for augmented u-net
    # **severstal_128, # resized to fit 128x128 size for augmented u-net
    #**cracks_datasets_reduced, # <-- svc(rbf,0.1,1)
    #**maipreform_datasets_reduced # <-- svc(rbf,0.1,1)
    **mvtec_tile_dataset,
    **mvtec_toothbrush,  # missing toothbrush dataset for later experimentation
    **cracks_datasets,
    **mvtec_cable_dataset,
    **metal_datasets,
    **textile_datasets,
    **mvtec_datasets,
    **aircarbon3_datasets_v2,
    **aircarbon3_datasets,
    **aircarbon2_datasets,
    **pultrusion_datasets,
    **severstal_plain,
    **spule_upside_0315,
    **maipreform_datasets
}

TEST_DATASETS = {**pultrusion_datasets}
