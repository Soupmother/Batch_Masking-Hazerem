import os
import fnmatch
from pci.masking import masking
from pci.hazerem import hazerem
from pci.pansharp2 import pansharp2
from pci.exceptions import *

# Set the working directory
working_dir = r'D:\PCI_Python\GLSvsL5\GLS2010'

# Set output directories
haze_output_dir = os.path.join(working_dir, '~Haze Removed')
if not os.path.isdir(haze_output_dir):
    os.mkdir(haze_output_dir)
    
# Set input file criteria - note that this list doens not contain a _mask.pix image previously created by 'masking', so
# is is not a useful operation for haze removal, but just a test to see where hazerem is going wrong
input_files = []

for r, d, f in os.walk(working_dir):
    for inFile in fnmatch.filter(f, '*_MTL.txt'):
        input_files.append(os.path.join(r, inFile))
        
# Remove the haze from both the multispectral and panchromatic bands
for image in input_files:
    try:
        hazerem(fili='-'.join([image, 'MS']),
                fili_pan='-'.join([image, 'PAN']),
                hazecov=[15],
                filo=os.path.join(haze_output_dir, '_haze_ms.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])),
                filo_pan=os.path.join(haze_output_dir, '_haze_pan.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e

