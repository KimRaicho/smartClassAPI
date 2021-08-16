import os
import cv2
import numpy as np


def data_acquisition(folder_path='/Final_Dataset'):
    cropped_images = []
    attentive_images = []
    not_attentive_images = []
    sleepy_images = []

    full_set_path = os.getcwd() + folder_path

    print('Reading Images...')
    for filename in os.listdir(full_set_path):
        image_name = (full_set_path + '//' + filename)
        class_name = filename.split('_')[0]

        if class_name == 'attentive':
            img = (image_crop(image_name))
            attentive_images.append(img)

        elif class_name == 'not':
            img = (image_crop(image_name))
            not_attentive_images.append(img)

        else:
            img = (image_crop(image_name))
            sleepy_images.append(img)

    #concatenate the arrays
    cropped_images = attentive_images + not_attentive_images + sleepy_images
        
    print('Done pre-processing images')
    return divide_datasets(cropped_images)


def image_crop(image_name):
    # read image as grayscale
    image = cv2.imread(image_name)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    cropped_image = cv2.resize(grayscale, (270, 540))

    return cropped_image


def normalize(data):
    shape = data.shape
    normalised_data = np.reshape(data, (shape[0], -1))
    normalised_data = normalised_data.astype('float32') / 255.  # scaling
    return np.reshape(normalised_data, shape)


def divide_datasets(array):
    training_set = []
    training_set_labels = []

    validation_set = []
    validation_set_labels = []

    testing_set = []
    testing_set_labels = []

    # training set
    i = 0
    j = 0
    k = 0
    m = 0
    for img in array:
        if i < 65:
            if j < 35:
                training_set.append(img)
                training_set_labels.append(0)
            elif j < 50:
                validation_set.append(img)
                validation_set_labels.append(0)
            else:
                testing_set.append(img)
                testing_set_labels.append(0)

            j += 1

        elif i < 126:
            if k < 42:
                training_set.append(img)
                training_set_labels.append(1)
            elif k < 52:
                validation_set.append(img)
                validation_set_labels.append(1)
            else:
                testing_set.append(img)
                testing_set_labels.append(1)

            k += 1

        else:
            if m < 27:
                training_set.append(img)
                training_set_labels.append(2)
            elif m < 32:
                validation_set.append(img)
                validation_set_labels.append(2)
            else:
                testing_set.append(img)
                testing_set_labels.append(2)

            m += 1

        i += 1

    print('Finished creating Datasets')

    # convert to numpy arrays and scale the images by 255
    training_set = np.asarray(training_set, dtype=np.uint8).reshape((104, 270, 540, 1))
    training_set = normalize(training_set)
    training_set_labels = np.asarray(training_set_labels, dtype=np.int).reshape(-1, 1)

    validation_set = np.asarray(validation_set, dtype=np.uint8).reshape((30, 270, 540, 1))
    validation_set = normalize(validation_set)
    validation_set_labels = np.asarray(validation_set_labels, dtype=np.int).reshape(-1, 1)

    testing_set = np.asarray(testing_set, dtype=np.uint8).reshape((30, 270, 540, 1))
    testing_set = normalize(testing_set)
    testing_set_labels = np.asarray(testing_set_labels, dtype=np.int).reshape(-1, 1)

    # save the numpy arrays to files
    np.save('datasets/train_x.npy', training_set)
    np.save('datasets/train_y.npy', training_set_labels)

    np.save('datasets/val_x.npy', validation_set)
    np.save('datasets/val_y.npy', validation_set_labels)

    np.save('datasets/test_x.npy', testing_set)
    np.save('datasets/test_y.npy', testing_set_labels)

    return training_set, training_set_labels, validation_set, validation_set_labels, testing_set, testing_set_labels
