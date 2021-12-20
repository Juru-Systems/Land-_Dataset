# %%
from shutil import copyfile,copy2
import glob, os
import cv2
import numpy as np
from PIL import Image
import json

# # Global variables

import_dir = '/content/Land_Dataset-main/base/'
export_dir = '/content/Land_Dataset-main/augmented/'


global dir
dir = {}

#loop through all the class folders
for folder in os.listdir(import_dir):
    dir[str(folder)] = {
        'path': import_dir + folder + '/',
        'imgs': {'originals' : glob.glob(import_dir + folder.lstrip("\\\\") + '/*.jpg')}
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
def increase_brightness(image_path, export_dir, label):
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

# %%
def decrease_brightness(image_path, export_dir, label):
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
        dir[folder]['imgs']['left_rotation'] = rotation(img, 90, export_dir + dir[folder]['path'], dir[folder])
        dir[folder]['imgs']['right_rotation'] = rotation(img, -90, export_dir + dir[folder]['path'], dir[folder])
        dir[folder]['imgs']['vertical_flip'] = vertical_flip(img, export_dir + dir[folder]['path'], dir[folder])
        dir[folder]['imgs']['increase_brightness'] = increase_brightness(img, export_dir + dir[folder]['path'], dir[folder])
        dir[folder]['imgs']['decrease_brightness'] = decrease_brightness(img, export_dir + dir[folder]['path'], dir[folder])
        dir[folder]['imgs']['sharpness'] = sharpness(img, export_dir + dir[folder]['path'], dir[folder])


#Save Directory Structure
with open('/content/Land_Dataset-main/augmented/directory.json', 'w+') as fp:
    json.dump(dir, fp, sort_keys=True, indent=4)

print(dir)
