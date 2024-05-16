# Placement Automation

## Overview and How to Use

There are 2 programs in this: one is for collecting data (main.py), the other's for the user to generate a final placement (mainn.py).

The ANN.py file is for training an ANN.

When the second program's configuration window is opened:
-The constraints put on Min Diff Dist, Gate Out Height, Diff Side Width range from 0.0 to 1.0.
-The units for Size Unit are: 'quetta', 'ronna', 'yotta', 'zetta', 'exa', 'peta', 'tera', 'giga', 'mega', 'kilo','hecto', 'deca', '-'
'deci', 'centi', 'milli', 'micro', 'nano', 'pico', 'femto', 'atto', 'zepto', 'yocto', 'ronto', 'quecto'
if the constraints of those lines aren't kept, they just become empty.

The constraints, if you want to insert them in a json file, you should do it in the config_data_ic.json file.

Honestly, the code isn't the best, but Idk if I'll ever clean the code. Sorry.

Unfortunately, the data.csv was cut in half (or less) due to GitHub's recommended max size.