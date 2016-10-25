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

    
# Set input file criteria  
input_files = []

for root, dirs, files in os.walk(working_dir):
    for inFile in fnmatch.filter(files, "*_MTL.txt"):   
        input_files.append(os.path.join(root, inFile))
       
# Create cloud, water and haze masks. 
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
        
# Haze removal. The problem with this is that I can't get the 'hazerem' script to recognise the mask file created
# by 'masking' (maskfili=). I have tried dozens of ways to make this work, but everything I come up with fails. Currently I'm trying to make a new list called 
# haze_input_files which adds files ending in _mask.pix to the list, and then defining mask as files with the "image" basename but .pix instead 
# of _MTL.txt. Unfortunately this results in no output by hazerem. Long story short, I changed the way I was making the list, and then it worked. And now it 
# doesn't work again, and I have no idea why. hazerem was working fine, and then I tried adding in the L% hazerem script - changed nothing in the L7 script
# - and now the whole fucking thing doesn't work any more. Fucking hell.
images = ['*_MTL.txt', '*_mask.pix']
matches = []

for root, dirnames, filenames in os.walk("working_dir"):
    for extensions in images:
        for filename in fnmatch.filter(filenames, extensions):
            matches.append(os.path.join(root, filename))        
        
for image in matches:
    try:
        hazerem(fili='-'.join([image, 'MS']),
                fili_pan='-'.join([image, 'PAN']),
                maskfili='.'.join([os.path.basename(image).split('_MTL')[0], 'pix']),
                hazecov=[15],
                filo=os.path.join(haze_output_dir, '_haze_ms.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])),
                filo_pan=os.path.join(haze_output_dir, '_haze_pan.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e       
        
# This batch of 'for' loops defines the sensor name (asensor) for the Landsat 5 images
for image in input_files:
    try:
        masking(fili='-'.join([image, 'MS']),
                maskfili='.'.join([os.path.basename(image).split('_MTL')[0], 'pix']),
                asensor="Landsat-5 TM",
                hazecov=[15],
                clthresh=[18,22,1],
                filo=os.path.join(masks_output_dir, '_mask.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e

# Makes new list including Landsat 5 Mask        
images = ['*_MTL.txt', '*_mask.pix']
matches = []

for root, dirnames, filenames in os.walk("working_dir"):
    for extensions in images:
        for filename in fnmatch.filter(filenames, extensions):
            matches.append(os.path.join(root, filename))

# Runs haze removal on the Landsat 5 images
for image in matches:
    try:
        hazerem(fili='-'.join([image, 'MS']),
                maskfili='.'.join([os.path.basename(image).split('_MTL')[0], 'pix']),
                asensor="Landsat-5 TM",
                hazecov=[15],
                filo=os.path.join(haze_output_dir, '_haze_ms.'.join([os.path.basename(image).split('_MTL')[0], 'pix'])))
    except PCIException, e:
        print e
    except Exception, e:
        print e                
