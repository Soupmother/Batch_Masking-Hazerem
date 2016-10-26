import os
import fnmatch
from pci.masking import masking
from pci.hazerem import hazerem
from pci.pansharp2 import pansharp2
from pci.exceptions import *

# Set the working directory
working_dir = r'D:\PCI_Python\GLSvsL5'


# Set output directories
masks_output_dir = os.path.join(working_dir, '~Masks')
if not os.path.isdir(masks_output_dir):
    os.mkdir(masks_output_dir)
    
haze_output_dir = os.path.join(working_dir, '~Haze Removed')
if not os.path.isdir(haze_output_dir):
    os.mkdir(haze_output_dir)    

final_output_dir = os.path.join(working_dir, '~Final Output')    
if not os.path.isdir(final_output_dir):
    os.mkdir(final_output_dir)

    
# Create 'input_files' list and set search criteria for 'os.walk'
input_files = []

for root, dirs, files in os.walk(working_dir):
    for inFile in fnmatch.filter(files, "*_MTL.txt"):   
        input_files.append(os.path.join(root, inFile))


# Create cloud, water and haze masks for Landsat 7 images
for image in input_files:
    try:
        masking(fili='-'.join([image, 'MS']),
                hazecov=[15],
                clthresh=[18,22,1],
                filo=os.path.join(masks_output_dir, '_mask.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e       

for image in input_files:
    try:
        masking(fili='-'.join([image, 'MS']),
                asensor="Landsat-5 TM",
                hazecov=[15],
                clthresh=[18,22,1],
                filo=os.path.join(masks_output_dir, '_mask.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e        

# Create new 'matches' list including '*.pix' output file from 'masking'        
#images = ['*_MTL.txt', '*_mask.pix']
#matches = []

#for root, dirnames, filenames in os.walk(working_dir):
#    for extensions in images:
#        for filename in fnmatch.filter(filenames, extensions):
#            matches.append(os.path.join(root, filename))

# Trying to build this list a different way:

in_dir = r'D:\PCI_Python\GLSvsL5'
img_filter = ['*_MTL.txt', '*_mask.pix']

def get_batch(in_dir, img_filter):
    for r, d, f in os.walk(in_dir):
        for in_file in fnmatch.filter(f, img_filter):
            yield os.path.join(r, in_file)            

# Run haze removal on Landsat 7 images using files from 'matches' list. The string defined for 'maskfili' is ugly as sin, and
# may be a source of this problem, but it's the only way I have figured out to tell hazerem that the mask file it's looking
# for in the input list (matches) is named like this:
#                                                    The basename of the file is L71132042_04220091031_MTL.txt
#                                                    os.path.basename(image)
#
#                                                    The name of the file hazerem (via maskfili) is looking for is 
#                                                    L71132042_04220091031_mask.pix
#                                                    So I tell maskfili to look for a file that is same as the basename, but 
#                                                    split before _MTL, and then joined to _mask.pix. I did that by figuring out 
#                                                    what the filo (output file) naming string was doing, and cutting it up. 
#                                                                                                   FUGLY
for image in get_batch:
    try:
        hazerem(fili='-'.join([image, 'MS']),
                fili_pan='-'.join([image, 'PAN']),
                maskfili='_mask.'.join([os.path.basename(image).split('_MTL')[0], 'pix']),
                asensor="Landsat-7 ETM+",
                hazecov=[15],
                filo=os.path.join(haze_output_dir, '_haze_ms.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])),
                filo_pan=os.path.join(haze_output_dir, '_haze_pan.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e       

# Runs haze removal on the Landsat 5 images
for image in get_batch:
    try:
        hazerem(fili='-'.join([image, 'MS']),
                maskfili='_mask.'.join([os.path.basename(image).split('_MTL')[0], 'pix']),
                asensor="Landsat-5 TM",
                hazecov=[15],
                filo=os.path.join(haze_output_dir, '_haze_ms.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e
