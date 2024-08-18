from param_tuning.hdev.hdev_operators_code import AREA_SIZE_THRESHOLD_HDEV, AUTO_THRESHOLD_HDEV, BINOMIAL_FILTER_HDEV, \
    FAST_THRESHOLD_HDEV, GRAY_CLOSING_HDEV, SOBEL_AMP_HDEV

"""
HDEV Function Lookup Dict
    contains all functions returned by cgp optimization digraph pipelines
    and allowing to get hdev code for bounds, parameters and partly hdev code
"""

PRIMES = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37]

HDEV_FUNCTION_LOOKUP = {
    'AreaSizeThreshold': {
        'name': 'area_size_threshold',
        'in': 'Image',
        'out': 'Region',
        'bounds': {
            'minGray': [15, 230],
            'maxGray': [230, 256],
            'minSize': [9000, 11000],
            'maxSize': [18000, 22000],
            'windowHeight': [160, 321],
            'windowWidth': [160, 321]
            },
        'hdev': AREA_SIZE_THRESHOLD_HDEV
    },
    'AutoThreshold': {
        'name': 'auto_threshold',
        'in': 'Image',
        'out': 'Region',
        'bounds': {
            'sigma': [0, 5]
        },
        'hdev': AUTO_THRESHOLD_HDEV
    },
    'BinomialFilter': {
        'name': 'binomial_filter',
        'in': 'Image',
        'out': 'Image',
        'bounds': {
            'maskWidth': PRIMES,
            'maskHeight': PRIMES
        },
        'hdev': BINOMIAL_FILTER_HDEV
    },
    """
    public int MinGray { get; set; } = 10;
    public int MaxGrayOffset { get; set; } = 200;
    public int MinSize { get; set; } = 2;
    """
    'FastThreshold': {
        'name': 'fast_threshold',
        'in': 'Image',
        'out': 'Region',
        'bounds': {
            'MinGray': [0, 254],
            'MaxGrayOffset': [0, 255],
            'MinSize': [0, 200]
        },
        'hdev': FAST_THRESHOLD_HDEV
    },
    'GrayClosing': {
        'name': 'fast_threshold',
        'in': 'Image',
        'out': 'Region',
        'bounds': {
            'A': [1, 5],
            'B': [1, 5],
            'GrayValueMax': [0, 255]
        },
        'hdev': GRAY_CLOSING_HDEV
    },
    'SobelAmp': {
        'name': 'sobel_amp',
        'in': 'Image',
        'out': 'Region',
        'bounds': {
            'filterType': None,
                # ['sum_abs', 'sum_abs_binomial', 'sum_sqrt', 'sum_sqrt_binomial', 'thin_max_abs',
                # 'thin_max_abs_binomial', 'thin_sum_abs', 'thin_sum_abs_binomial',
                # 'x', 'x_binomial', 'y', 'y_binomial']
            'maskSize': PRIMES
        },
        'hdev': SOBEL_AMP_HDEV
    },
}