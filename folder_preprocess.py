import os
from PIL import Image

filepath = 'database'

for folder_name in os.listdir(filepath):

    img_path = filepath + '/' + folder_name

    i = 35  # attentive
    j = 32  # not attentive
    k = 30  # sleepy

    for img in os.listdir(img_path):
        if folder_name == 'attentive':
            name = 'Final_Dataset/attentive_' + str(i)
            final_img = Image.open(img_path + '/' + img)
            final_img = final_img.resize((270, 540))
            final_img.save(name + '.jpeg')
            i += 1

        if folder_name == 'not_attentive':
            name = 'Final_Dataset/not_attentive_' + str(j)
            final_img = Image.open(img_path + '/' + img)
            final_img = final_img.resize((270, 540))
            final_img.save(name + '.jpeg')
            j += 1

        if folder_name == 'sleepy':
            name = 'Final_Dataset/sleepy_' + str(k)
            final_img = Image.open(img_path + '/' + img)
            final_img = final_img.resize((270, 540))
            final_img.save(name + '.jpeg')
            k += 1
