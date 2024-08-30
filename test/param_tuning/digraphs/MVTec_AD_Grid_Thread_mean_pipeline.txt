dataset: MVTec_AD_Grid_Thread

experiment_id: 107
run_id: 107
fit_values: [0.44745383165345565]
pipeline_id: 291

digraph:
digraph Pipeline { 
rankdir = "RL";91 [label="Closing\nA=27\n B=7\n C=0,392699\n StructElementType=Rectangle"];
78 [label="Union1\n"];
69 [label="Opening\nStructElement=Ellipse\n A=21\n B=20"];
20 [label="CropRectangle\nMinRatio=0,0399999991059303\n MaskHeight=13\n MaskWidth=19"];
36 [label="Union2\n"];
1 [label="CropSmallestRectangle\nMinGray=19\n MaxGray=255"];
22 [label="AutoThreshold\nSigma=0,5"];
_1 [label="HalconInputNode\nProgramInputIdentifier=-1"];
19 [label="SobelAmp\nFilterType=y\n MaskSize=7"];
91 -> 78 [];
78 -> 69 [];
69 -> 20 [];
69 -> 36 [];
20 -> 1 [];
36 -> 20 [];
36 -> 22 [];
1 -> _1 [];
22 -> 19 [];
19 -> 1 [];
}
