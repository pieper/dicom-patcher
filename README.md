# dicom-patcher
A python script to run [Slicer's DICOMPatcher](https://slicer.readthedocs.io/en/latest/user_guide/module_dicompatcher.html) from the command line

## Example
```
export SLICER=/Applications/Slicer-2020-04-12.app/Contents/MacOS/Slicer
$SLICER --no-main-window --python-script ~/slicer/latest/SlicerMorph/patch.py -- --same-names --normalize --input dicom_data --output dicom_data-patched/
```
## Usage
```
usage: dicom-patcher.py [-h] [--normalize] [--same-names] [--generate-missing]
                        [--position-from-thickness] [--partially-anonymize]
                        [--input INPUT] [--output OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --normalize           Replace file and folder names with automatically
                        generated names. Fixes errors caused by file path
                        containins special characters or being too long.
  --same-names          Generate patient name and ID from the first file in a
                        directory
  --generate-missing    Generate missing patient, study, series IDs. It is
                        assumed that all files in a directory belong to the
                        same series. Fixes error caused by too aggressive
                        anonymization
  --position-from-thickness
                        Generate 'image position sequence' for multi-frame
                        files that only have 'SliceThickness' field. Fixes
                        error in Dolphin 3D CBCT scanners.
  --partially-anonymize
                        Some patient identifiable information will be removed
                        from the patched DICOM files. There are many fields
                        that can identify a patient, this function does not
                        remove all of them.
  --input INPUT         Input DICOM directory
  --output OUTPUT       Output directory
  ```
