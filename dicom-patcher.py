
usage = """
export SLICER=/Applications/Slicer-2020-04-12.app/Contents/MacOS/Slicer
$SLICER --no-main-window --python-script ~/slicer/latest/SlicerMorph/patch.py -- --same-names --normalize --input dicom_data --output dicom_data-patched/
"""



import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--normalize", help="Replace file and folder names with automatically generated names.  Fixes errors caused by file path containins special characters or being too long.", action="store_false")
parser.add_argument("--same-names", help="Generate patient name and ID from the first file in a directory", action="store_true")
parser.add_argument("--generate-missing", help="Generate missing patient, study, series IDs. It is assumed that all files in a directory belong to the same series. Fixes error caused by too aggressive anonymization", action="store_false")
parser.add_argument("--position-from-thickness", help="Generate 'image position sequence' for multi-frame files that only have 'SliceThickness' field. Fixes error in Dolphin 3D CBCT scanners.", action="store_false")
parser.add_argument("--partially-anonymize", help="Some patient identifiable information will be removed from the patched DICOM files. There are many fields that can identify a patient, this function does not remove all of them.", action="store_true")

parser.add_argument("--input", help="Input DICOM directory")
parser.add_argument("--output", help="Output directory")

args = parser.parse_args()

import DICOMPatcher
logic = DICOMPatcher.DICOMPatcherLogic()

logic.clearRules()

if args.same_names:
    print("Adding Rule ForceSamePatientNameIdInEachDirectory")
    logic.addRule("ForceSamePatientNameIdInEachDirectory")

if args.generate_missing:
    print("Adding Rule GenerateMissingIDs")
    print("Adding Rule RemoveDICOMDIR")
    print("Adding Rule FixPrivateMediaStorageSOPClassUID")
    logic.addRule("GenerateMissingIDs")
    logic.addRule("RemoveDICOMDIR")
    logic.addRule("FixPrivateMediaStorageSOPClassUID")

if args.position_from_thickness:
    print("Adding Rule AddMissingSliceSpacingToMultiframe")
    logic.addRule("AddMissingSliceSpacingToMultiframe")

if args.partially_anonymize:
    print("Adding Rule Anonymize")
    logic.addRule("Anonymize")

if args.normalize:
    print("Adding Rule NormalizeFileNames")
    logic.addRule("NormalizeFileNames")

logic.patchDicomDir(args.input, args.output)

exit()
