import os
import sys

usage = """
 export SLICER=/Applications/Slicer-2020-04-12.app/Contents/MacOS/Slicer
 $SLICER --no-main-window --python-script dicom-to-nrrd.py -- --input dicom-data --output file.nrrd
"""
# adapted from
# https://github.com/QIICR/dcmheat/blob/master/docker/SlicerConvert.py

def setDICOMReaderApproach(approach):
    import DICOMScalarVolumePlugin
    approaches = DICOMScalarVolumePlugin.DICOMScalarVolumePluginClass.readerApproaches()
    if approach not in approaches:
        raise ValueError("Unknown dicom approach: %s\nValid options are: %s" % (approach, approaches))
    approachIndex = approaches.index(approach)
    settings = qt.QSettings()
    settings.setValue('DICOM/ScalarVolume/ReaderApproach', approachIndex)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--dcmtk", help="use dcmtk to parse dicom (exclusive with --gdcm)", action="store_true")
parser.add_argument("--gdcm", help="use dcmtk to parse dicom (exclusive with --dcmtk)", action="store_true")
parser.add_argument("--no-quit", help="For debugging, don't exit Slicer after converting", action="store_true")
parser.add_argument("--input", help="Input DICOM directory")
parser.add_argument("--output", help="Where to write nrrd file")

args = parser.parse_args()
if args.dcmtk and args.gdcm:
    raise ValueError("Cannot specify both gdcm and dcmtk")
if args.dcmtk:
    setDICOMReaderApproach('DCMTK')
if args.gdcm:
    setDICOMReaderApproach('GDCM')

from DICOMLib import DICOMUtils

loadedNodeIDs = []
with DICOMUtils.TemporaryDICOMDatabase() as db:
  DICOMUtils.importDicom(args.input, db)
  patientUIDs = db.patients()
  for patientUID in patientUIDs:
    loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))

if len(loadedNodeIDs)>1:
    print("Input dataset resulted in more than one scalar node! Aborting.")
    sys.exit(-1)
elif len(loadedNodeIDs)==0:
    print("No scalar volumes parsed from the input DICOM dataset! Aborting.")
    sys.exit(-2)
else:
    print('Saving to ', args.output)
    node = slicer.util.getNode(loadedNodeIDs[0])
    slicer.util.saveNode(node, args.output)

sys.exit(0)
