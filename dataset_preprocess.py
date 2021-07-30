import os
import cv2
import numpy as np


def data_acquisition(folder_path='\Final_Dataset'):
    cropped_images = []

    full_set_path = os.getcwd() + folder_path

    print('Reading Images...')
    num = 1
    for filename in os.listdir(full_set_path):
        image_name = (full_set_path + '\\' + filename)

        # resize the image
        img = (image_crop(image_name))
        cropped_images.append(img)
        num += 1
    print('Done pre-processing images')
    return divide_datasets(cropped_images)


def image_crop(image_name):
    # read image as grayscale
    image = cv2.imread(image_name, 0)

    cropped_image = cv2.resize(image, (270, 540))

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
    for img in os.listdir('Final_Dataset'):
        name = img.split('_')

        if name[0] == 'attentive':
            i = int(name[1])

            while i < 18:
                training_set.append(img)
                training_set_labels.append(0)
                i += 1

            while i < 23:
                validation_set.append(img)
                validation_set_labels.append(0)
                i += 1

            while i < 28:
                testing_set.append(img)
                testing_set_labels.append(0)
                i += 1

        if name[0] == 'not_attentive':
            i = int(name[1])

            while i < 13:
                training_set.append(img)
                training_set_labels.append(0)
                i += 1

            while i < 18:
                validation_set.append(img)
                validation_set_labels.append(0)
                i += 1

            while i < 23:
                testing_set.append(img)
                testing_set_labels.append(0)
                i += 1

        if name[0] == 'sleepy':
            i = int(name[1])

            while i < 14:
                training_set.append(img)
                training_set_labels.append(0)
                i += 1

            while i < 19:
                validation_set.append(img)
                validation_set_labels.append(0)
                i += 1

            while i < 24:
                testing_set.append(img)
                testing_set_labels.append(0)
                i += 1

    # convert to numpy arrays and scale the images by 255
    training_set = np.asarray(training_set, dtype=np.uint8).reshape((800, 272, 544, 1))
    training_set = normalize(training_set)
    training_set_labels = np.asarray(training_set_labels, dtype=np.int).reshape(-1, 1)

    validation_set = np.asarray(validation_set, dtype=np.uint8).reshape((400, 272, 544, 1))
    validation_set = normalize(validation_set)
    validation_set_labels = np.asarray(validation_set_labels, dtype=np.int).reshape(-1, 1)

    testing_set = np.asarray(testing_set, dtype=np.uint8).reshape((400, 272, 544, 1))
    testing_set = normalize(testing_set)
    testing_set_labels = np.asarray(testing_set_labels, dtype=np.int).reshape(-1, 1)

    # save the numpy arrays to files
    np.save('train_x.npy', training_set)
    np.save('train_y.npy', training_set_labels)

    np.save('val_x.npy', validation_set)
    np.save('val_y.npy', validation_set_labels)

    np.save('test_x.npy', testing_set)
    np.save('test_y.npy', testing_set_labels)

    return training_set, training_set_labels, validation_set, validation_set_labels, testing_set, testing_set_labels
