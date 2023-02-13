AvgOffspringFit_0 = \
    '[ ' \
    '{ ' \
    '"Generation": -1, ' \
    '"AverageOffspringFitness": 0.0 ' \
    '}, ' \
    '{ ' \
    '"Generation": 0, ' \
    '"AverageOffspringFitness": 0.051202207297239531 ' \
    '}, ' \
    '{ ' \
    '"Generation": 1, ' \
    '"AverageOffspringFitness": 0.0' \
    '}' \
    ']'

AvgPopulationFit_0 = \
    '[ ' \
    '{ ' \
    '"Generation": -1, ' \
    '"AveragePopulationFitness": 0.0 ' \
    '}, ' \
    '{ ' \
    '"Generation": 0, ' \
    '"AveragePopulationFitness": 0.0 ' \
    '}, ' \
    '{ ' \
    '"Generation": 1, ' \
    '"AveragePopulationFitness": 0.0' \
    '}' \
    ']'

BestIndividualFit_0 = \
    '[ ' \
    '{ ' \
    '"Generation": -1, ' \
    '"AverageIndividualFitness": 0.0 ' \
    '}, ' \
    '{ ' \
    '"Generation": 0, ' \
    '"AverageIndividualFitness": 0.0 ' \
    '}, ' \
    '{ ' \
    '"Generation": 1, ' \
    '"AverageIndividualFitness": 0.0' \
    '}' \
    ']'

EVOLUTIONSTRATEGY_TXT = \
    '<?xml version="1.0" encoding="utf-8"?>' \
    '<ESConfiguration xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' \
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
    '<Rho>0</Rho>' \
    '<Lambda>4</Lambda>' \
    '<PlusSelection>true</PlusSelection>' \
    '<Mu>1</Mu>' \
    '</ESConfiguration>'

FITNESS_TXT = \
    '<?xml version="1.0" encoding="utf-8"?>' \
    '<HalconFitnessConfiguration xmlns:xsd="http://www.w3.org/2001/XMLSchema" ' \
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">' \
    '<RegionScoreWeight>0</RegionScoreWeight>' \
    '<ArtifactScoreWeight>0</ArtifactScoreWeight>' \
    '<FitnessScoreWeight>1</FitnessScoreWeight>' \
    '<Maximization>true</Maximization>' \
    '<Weights>' \
    '<double>1</double>' \
    '</Weights>' \
    '<FitnessFunctions>' \
    '<FitnessFunction>MCC</FitnessFunction>' \
    '</FitnessFunctions>' \
    '<ExcessRegionHandling>None</ExcessRegionHandling>' \
    '<RegionCountThreshold xsi:nil="true" />' \
    '<ExecutionTimeThreshold xsi:nil="true" />' \
    '<UseExecutionTimeFitnessPenalty>false</UseExecutionTimeFitnessPenalty>' \
    '<ExecutionTimeFunctionScaleFactor>0</ExecutionTimeFunctionScaleFactor>' \
    '<PixelPercentageThreshold>0.699999988079071</PixelPercentageThreshold>' \
    '<Filename>/Default/</Filename>' \
    '</HalconFitnessConfiguration>'

GRID_TXT = \
    'HashCode: 1196554941\n' \
    'Time: 2/1/2023 9:30:31 AM\n' \
    'System.Exception, ignore this, \n' \
    'Inputs: -1 \n' \
    '0: IN: -1 HighpassImage(493,229,57,0,0,0)                | 10: IN: 2 SobelAmp(2,5,0,0,0,0)                          | {{20: IN: 5 LocalThreshold(0,0,31,0.2,0,0)}}             | {{30: IN: 20 Closing(0,14,30,-0.392699,0,0)}}            | 40: IN: 22 ExpandGray(4,1,50,0,0,0)                      | 50: IN: 9 29 CloseEdges(235,0,0,0,0,0)                   | 60: IN: 29 SelectShape(9,79,27,9,0,0)                    | 70: IN: 68 Dilation1(2,2,26,10,0,0)                      | 80: IN: 9 CropRectangle(13,29,0.02,100,0,0)              | 90: IN: 78 59 Opening(0,28,17,12,0,0)                    | \n' \
    '1: IN: -1 CoherenceEnhancingDiff(0.4,1,0.2,355,0,0)      | 11: IN: -1 SobelAmp(0,3,0,0,0,0)                         | 21: IN: 13 VarThreshold(19,7,-0.8,62,1,0)                | 31: IN: 25 AreaToRectangle(17,2,27,17,0,0)               | 41: IN: 24 1 HistoToThresh(3,0,0,0,0,0)                  | 51: IN: 16 20 CloseEdges(86,0,0,0,0,0)                   | {{61: IN: 30 58 Opening(1,15,13,0,0,0)}}                 | 71: IN: 42 Union1(2,18,3,1.178097,0,0)                   | 81: IN: 17 FastThreshold(214,93,47,1000,0,0)             | 91: IN: 51 77 Opening(0,21,10,19,0,0)                    | \n' \
    '2: IN: -1 MedianImage(10,0,60,312,0,0)                   | 12: IN: 6 SobelAmp(0,5,0,0,0,0)                          | 22: IN: 16 ThresholdAccessChannel(10,-1,1,0.2,0,0)       | 32: IN: 22 AreaToRectangle(9,38,8,0,0,0)                 | 42: IN: 39 ExpandGray(10,0,10,0,0,0)                     | 52: IN: 15 28 CloseEdges(179,0,0,0,0,0)                  | 62: IN: 47 AreaToRectangle(0,7,17,-0.785398,0,0)         | 72: IN: 29 Erosion1(2,0,27,24,0,0)                       | 82: IN: -1 VarThreshold(9,19,0.3000001,15,0,0)           | 92: IN: 47 Closing(0,24,21,-0.392699,0,0)                | \n' \
    '3: IN: -1 EliminateMinMax(31,23,40,1,0,0)                | 13: IN: 1 SobelAmp(1,7,0,0,0,0)                          | 23: IN: 5 RegionGrowing(11,3,6,500,0,0)                  | 33: IN: 29 Erosion1(33,0,7,12,0,0)                       | 43: IN: 32 ExpandGray(9,0,10,0,0,0)                      | 53: IN: 2 23 CloseEdges(139,0,0,0,0,0)                   | 63: IN: 52 30 Union2(0,0,0,0,0,0)                        | 73: IN: 36 54 Union2(47,0,19,19,0,0)                     | 83: IN: 4 LocalThreshold(0,1,31,0.2,0,0)                 | 93: IN: 76 SelectShape(6,78,19,30,0,0)                   | \n' \
    '4: IN: -1 SobelAmp(0,5,1,0,0,0)                          | {{14: IN: 8 SobelAmp(0,3,0,0,0,0)}}                      | 24: IN: 6 AutoThreshold(0.5,247,10000,18000,280,320)     | 34: IN: 28 AreaToRectangle(3,1,24,10,0,0)                | 44: IN: 37 ExpandGray(4,1,10,0,0,0)                      | 54: IN: 5 31 CloseEdges(127,0,0,0,0,0)                   | 64: IN: 49 Erosion1(49,1,4,13,0,0)                       | 74: IN: 35 37 Opening(2,10,9,19,0,0)                     | 84: IN: 0 FastThreshold(235,253,182,0,0,0)               | 94: IN: 29 73 Opening(2,23,13,-0.785398,0,0)             | \n' \
    '{{5: IN: -1 HighpassImage(327,419,0,0,0,0)}}             | 15: IN: -1 SobelAmp(2,5,0,0,0,0)                         | 25: IN: 16 RegionGrowing(21,3,3,1,0,0)                   | 35: IN: 24 25 Union2(2,4,20,0,0,0)                       | 45: IN: 35 9 HistoToThresh(3,0,0,0,0,0)                  | 55: IN: 18 29 CloseEdges(143,0,0,0,0,0)                  | 65: IN: 36 43 Union2(2,10,13,0,0,0)                      | 75: IN: 60 AreaToRectangle(7,85,6,16,0,0)                | 85: IN: 1 FastThreshold(21,62,178,0,0,0)                 | 95: IN: 31 Dilation1(16,2,28,28,0,0)                     | \n' \
    '6: IN: -1 SigmaImage(13,7,244,3,0,0)                     | 16: IN: 7 SobelAmp(2,5,0,0,0,0)                          | 26: IN: 18 Threshold(15,225,5,200,0,0)                   | 36: IN: 29 Union1(30,2,7,6,0,0)                          | 46: IN: 22 13 HistoToThresh(2,1,15,0,0,0)                | 56: IN: 1 22 CloseEdges(229,0,0,0,0,0)                   | 66: IN: 59 Union1(1,2,11,0,0,0)                          | 76: IN: 59 56 Opening(2,27,16,-0.785398,0,0)             | 86: IN: 18 RegionGrowing(5,9,4,1000,220,160)             | 96: IN: 43 AreaToRectangle(50,0,7,5,0,0)                 | \n' \
    '7: IN: -1 GrayClosing(6,19,20,0,0,0)                     | 17: IN: 3 SobelAmp(2,3,0,0,0,0)                          | 27: IN: 0 AutoThreshold(4,253,10000,19000,240,170)       | 37: IN: 24 Union1(2,19,29,0,0,0)                         | 47: IN: 24 ExpandGray(4,0,15,0,0,0)                      | 57: IN: 4 34 CloseEdges(55,0,0,0,0,0)                    | 67: IN: 27 SelectShape(10,24,10,20,0,0)                  | 77: IN: 64 Closing(0,22,13,0.392699,0,0)                 | 87: IN: 1 AutoThreshold(2,-1,1,0.3,0,0)                  | 97: IN: 45 78 Union2(1,20,11,0.392699,0,0)               | \n' \
    '{{8: IN: -1 GrayOpening(11,6,5,0,0,0)}}                  | 18: IN: 9 SobelAmp(3,7,0,0,0,0)                          | 28: IN: 8 ZeroCrossing(3,-1,2,19000,240,270)             | 38: IN: 20 Closing(2,14,1,0,0,0)                         | 48: IN: 28 ExpandGray(10,1,5,0,0,0)                      | {{58: IN: 14 20 CloseEdges(152,0,0,0,0,0)}}              | 68: IN: 38 Closing(0,16,26,0.392699,0,0)                 | 78: IN: 31 Union1(8,11,14,-0.392699,0,0)                 | 88: IN: 13 AutoThreshold(5,0,0,0,0,0)                    | 98: IN: 22 SelectShape(7,29,0,0,0,0)                     | \n' \
    '9: IN: -1 Laplace(13,0,0,0,0,0)                          | 19: IN: 5 SobelAmp(3,7,0,0,0,0)                          | 29: IN: 6 BinaryThreshold(0,0,0.065,0,0,0)               | 39: IN: 25 Connection(8,32,0,0,0,0)                      | 49: IN: 39 ExpandGray(5,1,50,0,0,0)                      | 59: IN: 5 31 CloseEdges(204,0,0,0,0,0)                   | 69: IN: 59 51 Union2(8,27,24,0,0,0)                      | 79: IN: 59 Union1(4,26,2,0,0,0)                          | 89: IN: -1 AreaSizeThreshold(23,247,10000,20000,240,300) | 99: IN: 44 Connection(4,7,14,-0.392699,0,0)              | \n' \
    'Outputs: 61 \n' \
    'active Nodes: 61 30 58 20 14 5 8 \n' \
    '_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________'

APPEND_PIPELINE_TXT = \
    'digraph Pipeline {' \
    'rankdir = "RL";61 [label="Opening\nStructElement=Rectangle\n A=15\n B=13"];' \
    '30 [label="Closing\nA=14\n B=30\n C=-0.392699\n StructElementType=Circle"];' \
    '58 [label="CloseEdges\nMinAmplitude=152"];' \
    '20 [label="LocalThreshold\nMethod=adapted_std_deviation\n LightDark=dark\n MaskSize=31\n Scale=0.2"];' \
    '14 [label="SobelAmp\nFilterType=y\n MaskSize=3"];' \
    '5 [label="HighpassImage\nMaskWidth=327\n MaskHeight=419"];' \
    '8 [label="GrayOpening\nStructElement=Circle\n A=11\n B=6\n GrayValueMax=5"];' \
    '_1 [label="HalconInputNode\nProgramInputIdentifier=-1"];' \
    '61 -> 30 [];' \
    '61 -> 58 [];' \
    '30 -> 20 [];' \
    '58 -> 20 [];' \
    '58 -> 14 [];' \
    '20 -> 5 [];' \
    '14 -> 8 [];' \
    '5 -> _1 [];' \
    '8 -> _1 [];' \
    '}'

VECTOR = '-1,0,30,493,229,57,0,0,0,-1,0,10,0.4,1,0.2,355,0,0,-1,0,37,10,0,60,312,0,0,-1,0,19,31,23,40,1,0,0,-1,0,45,' \
         '0,5,1,0,0,0,-1,0,30,327,419,0,0,0,0,-1,0,43,13,7,244,3,0,0,-1,0,25,6,19,20,0,0,0,-1,0,28,11,6,5,0,0,0,-1,0,' \
         '33,13,0,0,0,0,0,2,0,45,2,5,0,0,0,0,-1,0,45,0,3,0,0,0,0,6,0,45,0,5,0,0,0,0,1,0,45,1,7,0,0,0,0,8,0,45,0,3,0,' \
         '0,0,0,-1,0,45,2,5,0,0,0,0,7,0,45,2,5,0,0,0,0,3,0,45,2,3,0,0,0,0,9,0,45,3,7,0,0,0,0,5,0,45,3,7,0,0,0,0,5,0,' \
         '35,0,0,31,0.2,0,0,13,0,51,19,7,-0.8,62,1,0,16,0,48,10,-1,1,0.2,0,0,5,0,40,11,3,6,500,0,0,6,0,4,0.5,247,' \
         '10000,18000,280,320,16,0,40,21,3,3,1,0,0,18,0,47,15,225,5,200,0,0,0,0,4,4,253,10000,19000,240,170,8,0,52,3,' \
         '-1,2,19000,240,270,6,0,6,0,0,0.065,0,0,0,20,0,9,0,14,30,-0.392699,0,0,25,0,3,17,2,27,17,0,0,22,21,3,9,38,8,' \
         '0,0,0,29,22,21,33,0,7,12,0,0,28,23,3,3,1,24,10,0,0,24,25,50,2,4,20,0,0,0,29,0,49,30,2,7,6,0,0,24,22,49,2,' \
         '19,29,0,0,0,20,24,9,2,14,1,0,0,0,25,0,11,8,32,0,0,0,0,22,13,22,4,1,50,0,0,0,24,1,31,3,0,0,0,0,0,39,17,22,' \
         '10,0,10,0,0,0,32,7,22,9,0,10,0,0,0,37,17,22,4,1,10,0,0,0,35,9,31,3,0,0,0,0,0,22,13,31,2,1,15,0,0,0,24,5,22,' \
         '4,0,15,0,0,0,28,16,22,10,1,5,0,0,0,39,0,22,5,1,50,0,0,0,9,29,8,235,0,0,0,0,0,16,20,8,86,0,0,0,0,0,15,28,8,' \
         '179,0,0,0,0,0,2,23,8,139,0,0,0,0,0,5,31,8,127,0,0,0,0,0,18,29,8,143,0,0,0,0,0,1,22,8,229,0,0,0,0,0,4,34,8,' \
         '55,0,0,0,0,0,14,20,8,152,0,0,0,0,0,5,31,8,204,0,0,0,0,0,29,45,42,9,79,27,9,0,0,30,58,39,1,15,13,0,0,0,47,0,' \
         '3,0,7,17,-0.785398,0,0,52,30,50,0,0,0,0,0,0,49,0,21,49,1,4,13,0,0,36,43,50,2,10,13,0,0,0,59,28,49,1,2,11,0,' \
         '0,0,27,0,42,10,24,10,20,0,0,38,0,9,0,16,26,0.392699,0,0,59,51,50,8,27,24,0,0,0,68,0,14,2,2,26,10,0,0,42,65,' \
         '49,2,18,3,1.178097,0,0,29,21,21,2,0,27,24,0,0,36,54,50,47,0,19,19,0,0,35,37,39,2,10,9,19,0,0,60,0,3,7,85,6,' \
         '16,0,0,59,56,39,2,27,16,-0.785398,0,0,64,50,9,0,22,13,0.392699,0,0,31,0,49,8,11,14,-0.392699,0,0,59,58,49,' \
         '4,26,2,0,0,0,9,0,12,13,29,0.02,100,0,0,17,0,23,214,93,47,1000,0,0,-1,0,51,9,19,0.3000001,15,0,0,4,0,35,0,1,' \
         '31,0.2,0,0,0,0,23,235,253,182,0,0,0,1,0,23,21,62,178,0,0,0,18,0,40,5,9,4,1000,220,160,1,0,4,2,-1,1,0.3,0,0,' \
         '13,0,4,5,0,0,0,0,0,-1,0,2,23,247,10000,20000,240,300,78,59,39,0,28,17,12,0,0,51,77,39,0,21,10,19,0,0,47,0,' \
         '9,0,24,21,-0.392699,0,0,76,41,42,6,78,19,30,0,0,29,73,39,2,23,13,-0.785398,0,0,31,0,14,16,2,28,28,0,0,43,0,' \
         '3,50,0,7,5,0,0,45,78,50,1,20,11,0.392699,0,0,22,78,42,7,29,0,0,0,0,44,0,11,4,7,14,-0.392699,0,0,61 '

IMAGES_0 = \
    '{' \
    '"00cdb56a0.jpg": {' \
    '  "true positives": 1133,' \
    '  "true negatives": 407157,' \
    '  "false positives": 0,' \
    '  "false negatives": 1310,' \
    '  "MCC": 0.67991666572020382,' \
    '  "height": 256,' \
    '  "width": 1600,' \
    '  "size total": 409600' \
    '},' \
    '"00e0398ad.jpg": {' \
    '  "true positives": 73136,' \
    '  "true negatives": 146731,' \
    '  "false positives": 171791,' \
    '  "false negatives": 17942,' \
    '  "MCC": 0.22361513048743209,' \
    '  "height": 256,' \
    '  "width": 1600,' \
    '  "size total": 409600' \
    '},' \
    '"000a4bcdd.jpg": {' \
    '  "true positives": 0,' \
    '  "true negatives": 397923,' \
    '  "false positives": 0,' \
    '  "false negatives": 11677,' \
    '  "MCC": 0.0,' \
    '  "height": 256,' \
    '  "width": 1600,' \
    '  "size total": 409600' \
    '}' \
    '}'

LEGEND_TXT = \
    'Red: actual (ist)' \
    'Green: reference (soll)' \
    'Yellow: intersection of actual and reference, i.e. true positives'

EXCEPTION_TXT = \
    '2023-01-31 10:19:39.239 +01:00 [INF] batch --backend=halcon --runs=2 ' \
    '--train-data-dir=/mnt/sdc1/evias_expmts/severstal-steel/train_cgp ' \
    '--val-data-dir=/mnt/sdc1/evias_expmts/severstal-steel/val_cgp --generations=150' \
    '2023-01-31 10:19:39.239 +01:00 [INF] Optimization.Commandline, Version=1.0.0.0, Culture=neutral, ' \
    'PublicKeyToken=null' \
    '2023-01-31 10:19:39.320 +01:00 [WRN] No seed was specified, seeding randomly.' \
    '2023-01-31 10:19:39.320 +01:00 [INF] Seed: 1804018924' \
    '2023-01-31 10:20:14.774 +01:00 [ERR] Optimization.Pipeline.CGPPipelineException: DefaultName caused an ' \
    'exception. ---> Optimization.Pipeline.OperatorException: Exception caused at: Union2: NodeID=99, ' \
    'Exception caused at: Dilation1: Iterations=13 StructElement=Circle A=28 B=15 NodeID=67, Exception caused at: ' \
    'CloseEdges: MinAmplitude=52 NodeID=55, CloseEdges expects one child to be of OperatorType.EdgeAmplitude ---> ' \
    'Optimization.Pipeline.OperatorException: Exception caused at: Dilation1: Iterations=13 StructElement=Circle A=28 ' \
    'B=15 NodeID=67, Exception caused at: CloseEdges: MinAmplitude=52 NodeID=55, CloseEdges expects one child to be ' \
    'of OperatorType.EdgeAmplitude ---> Optimization.Pipeline.OperatorException: Exception caused at: CloseEdges: ' \
    'MinAmplitude=52 NodeID=55, CloseEdges expects one child to be of OperatorType.EdgeAmplitude ---> ' \
    'System.Exception: CloseEdges expects one child to be of OperatorType.EdgeAmplitude '
