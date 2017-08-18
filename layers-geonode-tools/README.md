# Data migration tools for LULC

## union_lulc.py

*Script for renaming and merging of LULC shapefiles*

```
union_lulc.py [-h] [-i INPUT_DIRECTORY] [-o OUTPUT_DIRECTORY]
```

### Requirements
```
ArcPy
Folder containing LULC shapefiles
```

### Arguments
* input_directory - contains input LULC shapefiles
* output_directory - location of renamed and merged shapefiles

1. Open command prompt
1. Change directory to the script location `cd [path\to\script\folder]`
1. Run this command: `union_lulc.py -i [path\to\input\folder] -o [path\to\output\folder]`

### Results

```
union_lulc.log - for logging purposes
union_lulc.csv - for monitoring purposes
