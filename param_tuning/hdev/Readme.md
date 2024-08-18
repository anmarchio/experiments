# Translating all HDEV Operators

## Workflow

1. Walk database for pipelines
2. Read pipelines and write them to a dict of node arrays each containing a dict of parameters, e.g.:

```
# hdev_functions.py
HDEV_LOOKUP = {
    'SobelAmp': {
        'name': 'sobel_amp',
        'in': 'Image',
        'out': 'Region',
        'bounds': [['sum_abs', 'sum_abs_binomial', 'sum_sqrt', 'sum_sqrt_binomial', 'thin_max_abs',
                    'thin_max_abs_binomial', 'thin_sum_abs', 'thin_sum_abs_binomial',
                    'x', 'x_binomial', 'y', 'y_binomial'],
                   PRIMES],
        'hdev': SOBEL_AMP_HDEV
    },
    (...)
}
```
3. Get the right HDEV code given the parameters from the digraph:
   * call `get_function_hdev_code` in `hdev_helpers.py` to get the right function code 
   * find in `HDEV_LOOKUP` dict (e.g. by referencing to `SobelAmp` key): `HDEV_LOOKUP['SobelAmp']`
   * get the code translation from subkey `'HDEV'` (which references a public variable in `hdev_operators_code.py`)
4. Check
   * Do the bounds in `HDEV_LOOPUP` have the right parameters?
   * Does `get_main_function_hdev_code` work properly?

### Update from 18-08-2024

As of 18-08-2024, implementation for this part has been stopped. 
If resumed, please note that the code has never been properly tested.