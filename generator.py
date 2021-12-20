import getopt
from shutil import copy2
import glob, os, sys
import cv2
import numpy as np
import json
import random
# # Global variables

import_dir = '/content/Land_Dataset-main/base/'
export_dir = '/content/Land_Dataset-main/augmented/'


global dir
dir = {}

#loop through all the class folders
for folder in os.listdir(import_dir):
    dir[str(folder)] = {
        'path': import_dir + folder + '/',
        'imgs': {'originals' : glob.glob(import_dir + folder + "/images" + '/*.jpg'),
                 'left_rotation' : [],
                 'right_rotation' : [],
                 'vertical_flip' : [],
                 'high_brightness' : [],
                 'low_brightness' : [],
                 'sharpness' : []}
    }



# # Image Augmentation Functions
# ## Rotations
def rotation(image_path, angle, export_dir, label):
    image = cv2.imread(image_path)
    #Transformation algorithm
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, scale=1)
    rotated_image = cv2.warpAffine(image,rotation_matrix,(width,height))
    
    num_id = len(os.listdir(export_dir)) + 1
    destination_file_name = label + str(num_id) + ".jpg"
    file_destination_path = export_dir +  destination_file_name
    
    cv2.imwrite(file_destination_path, rotated_image)
    return file_destination_path

# ## Vertical Flips
def vertical_flip(image_path, export_dir, label):
    image = cv2.imread(image_path)
    #Transformation algorithm
    flipped_img = cv2.flip(image, 0)
    
    num_id = len(os.listdir(export_dir)) + 1
    destination_file_name = label + str(num_id) + ".jpg"
    file_destination_path = export_dir +  destination_file_name
    
    cv2.imwrite(file_destination_path, flipped_img)
    return file_destination_path


# ### High Brightness
def high_brightness(image_path, export_dir, label):
    image = cv2.imread(image_path)
    #Transformation algorithm
    bright = np.ones(image.shape , dtype="uint8") * 70
    brightincrease = cv2.add(image,bright)
    
    num_id = len(os.listdir(export_dir)) + 1
    destination_file_name = label + str(num_id) + ".jpg"
    file_destination_path = export_dir +  destination_file_name
    
    cv2.imwrite(file_destination_path, brightincrease)
    print(file_destination_path, " Created")
    return file_destination_path

def low_brightness(image_path, export_dir, label):
    image = cv2.imread(image_path)
    #Transformation algorithm
    bright = np.ones(image.shape , dtype="uint8") * 70
    brightdecrease = cv2.subtract(image,bright)
    
    num_id = len(os.listdir(export_dir)) + 1
    destination_file_name = label + str(num_id) + ".jpg"
    file_destination_path = export_dir +  destination_file_name
    
    cv2.imwrite(file_destination_path, brightdecrease)
    return file_destination_path

# ## Sharpness Image Augmention
def sharpness(image_path, export_dir, label):
    image = cv2.imread(image_path)
    #Transformation algorithm
    sharpening = np.array([ [-1,-1,-1],
                            [-1,10,-1],
                            [-1,-1,-1] ])
    sharpened = cv2.filter2D(image,-1,sharpening)
    
    num_id = len(os.listdir(export_dir)) + 1
    destination_file_name = label + str(num_id) + ".jpg"
    file_destination_path = export_dir +  destination_file_name
    
    cv2.imwrite(file_destination_path, sharpened)
    return file_destination_path




# # Implementation
for folder in dir:
    for img in dir[folder]['imgs']['originals']:
        dir[folder]['imgs']['left_rotation'].append(rotation(img, 90, dir[folder]['path'] + 'images/', str(folder)))
        dir[folder]['imgs']['right_rotation'].append(rotation(img, -90, dir[folder]['path'] + 'images/', str(folder)))
        dir[folder]['imgs']['vertical_flip'].append(vertical_flip(img, dir[folder]['path'] + 'images/', str(folder)))
        dir[folder]['imgs']['high_brightness'].append(high_brightness(img, dir[folder]['path'] + 'images/', str(folder)))
        dir[folder]['imgs']['low_brightness'].append(low_brightness(img, dir[folder]['path'] + 'images/', str(folder)))
        dir[folder]['imgs']['sharpness'].append(sharpness(img, dir[folder]['path'] + 'images/', str(folder)))


#Save Directory Structure
with open('/content/Land_Dataset-main/augmented/directory.json', 'w+') as fp:
    json.dump(dir, fp, sort_keys=True, indent=4)


dataset = {}

training_dir = {}
validation_dir = {}
test_dir = {}

#Gather Dataset Structure & paths
for folder in dir:
    dataset[str(folder)] = []
    for img in random.shuffle(os.listdir(dir[folder]['path'] + 'images/')):
        dataset[folder].apped(dir[folder]['path'] + 'images/' + img)

    dataset[str(folder)] = random.shuffle(dataset[str(folder)])

#split dataset into training, validation, and test sets
training_dir = dataset[:int(len(dataset) * 0.7)]
validation_dir = dataset[int(len(dataset) * 0.7):int(len(dataset) * 0.9)]
test_dir = dataset[int(len(dataset) * 0.9):]




# argumentList = sys.argv[1:]
 
# # Options
# options = "hmo:"
 
# # Long options
# long_options = ["help", "shuffle", "ratio"]
 
# try:
#     # Parsing argument
#     arguments, values = getopt.getopt(argumentList, options, long_options)
     
#     # checking each argument
#     for currentArgument, currentValue in arguments:
 
#         if currentArgument in ("-h", "--help"):
#             print ("Displaying Help")
             
#         elif currentArgument in ("-s", "--Shuffle"):
#             print ("Displaying file_name:", sys.argv[0])
             
#         elif currentArgument in ("-r", "--ratio"):
#             print (("Enabling special output mode (% s)") % (currentValue))
             
# except getopt.error as err:
    # output error, and return with an error code
    print (str(err))