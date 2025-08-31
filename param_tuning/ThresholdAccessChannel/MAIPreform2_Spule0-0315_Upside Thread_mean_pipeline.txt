dataset: MAIPreform2_Spule0-0315_Upside Thread

experiment_id: 182
run_id: 182
fit_values: [0.12973488277429515]
pipeline_id: 371

digraph:
digraph Pipeline { 
rankdir = "RL";84 [label="ThresholdAccessChannel\nChannel=1\n Threshold=41\n Sign=-1"];
0 [label="GrayClosing\nStructElement=Circle\n A=28\n B=27\n GrayValueMax=40"];
_1 [label="HalconInputNode\nProgramInputIdentifier=-1"];
84 -> 0 [];
0 -> _1 [];
}
