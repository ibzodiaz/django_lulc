import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from sklearn.preprocessing import MinMaxScaler

from patchify import patchify, unpatchify


def get_image_dataset(image):
    scaler = MinMaxScaler()
    patch_size = 256

    #image = cv2.imread(path+"/"+image_name,1)

    h,w = image.shape[:-1]
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    SIZE_X = (image.shape[1]//patch_size)*patch_size
    SIZE_Y = (image.shape[0]//patch_size)*patch_size
    image = Image.fromarray(image)
    image = image.crop((0,0,SIZE_X,SIZE_Y))
    image = np.array(image)
    patches_img = patchify(image, (patch_size, patch_size, 3), step=patch_size)

    image_dataset =[]
    for i in range(patches_img.shape[0]):
        for j in range(patches_img.shape[1]):
            single_patch_img = patches_img[i,j,0,:,:]
            single_patch_img = scaler.fit_transform(single_patch_img.reshape(-1, single_patch_img.shape[-1])).reshape(single_patch_img.shape)
            image_dataset.append(single_patch_img)

    return (image_dataset,patches_img,h,w)


def get_image_dataset_for_video(image):
    scaler = MinMaxScaler()
    patch_size = 256

    h,w = image.shape[:-1]
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    SIZE_X = (image.shape[1]//patch_size)*patch_size
    SIZE_Y = (image.shape[0]//patch_size)*patch_size
    image = Image.fromarray(image)
    image = image.crop((0,0,SIZE_X,SIZE_Y))
    image = np.array(image)
    patches_img = patchify(image, (patch_size, patch_size, 3), step=patch_size)

    image_dataset =[]
    for i in range(patches_img.shape[0]):
        for j in range(patches_img.shape[1]):
            single_patch_img = patches_img[i,j,0,:,:]
            single_patch_img = scaler.fit_transform(single_patch_img.reshape(-1, single_patch_img.shape[-1])).reshape(single_patch_img.shape)
            image_dataset.append(single_patch_img)

    return (image_dataset,image,patches_img,h,w)

def reconstruct_image_from_patches(patch_list, input_image_shape, patch_size):
    input_image_width, input_image_height = input_image_shape

    num_rows = (input_image_height) // (patch_size[0]) * patch_size[0]
    num_cols = (input_image_width) // (patch_size[1]) * patch_size[1]

    # Créer une image vide pour la reconstitution
    image_reconstituee = np.zeros((num_rows, num_cols), dtype=patch_list[0].dtype)

    # Remplir l'image reconstituée avec les patches
    index = 0
    for y in range(0, num_rows, patch_size[0]):
        for x in range(0, num_cols, patch_size[1]):
            image_reconstituee[y:y + patch_size[0], x:x + patch_size[1]] = patch_list[index]
            index += 1

    return image_reconstituee

def convert_2D_label_to_rgb(mask):

    value_to_color = {
      4: (60, 16, 152),  # Building
      1: (254, 221, 58),  # Vegetation
      2: (226, 169, 41),  # Water
      3: (110, 193, 228),  # Road
      0: (132, 41, 246),  # Land
      5: (0, 255, 35),  # Cultivated_Field
      6: (255, 0, 0),  # Uncultivated_Field
      7: (0, 0, 255)  # Football_field
    }

    # Créez un tableau vide pour stocker les couleurs
    colorized_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    # Remplacez les valeurs dans mask2 par les couleurs correspondantes
    for value, color in value_to_color.items():
        colorized_mask[mask == value] = color

    return colorized_mask

def mask_repartition(mask):
    class_colors = {
        'Building': (60, 16, 152),
        'Land': (132, 41, 246),
        'Road': (110, 193, 228),
        'Vegetation': (254, 221, 58),
        'Water': (226, 169, 41),
        'cultivated field': (0, 255, 35),
        'uncultivated field': (255, 0, 0),
        'Football field': (0, 0, 255)
    }

    class_pixel_counts = {cls: 0 for cls in class_colors.keys()}

    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

    for cls, color in class_colors.items():
        class_mask = np.all(mask == np.array(color), axis=-1)
        class_pixel_count = np.sum(class_mask)
        class_pixel_counts[cls] += class_pixel_count

    total_pixels = sum(class_pixel_counts.values())

    if total_pixels == 0:
        raise ValueError("Aucun pixel correspondant aux couleurs des classes n'a été trouvé dans le masque.")

    class_percentages = {cls: count / total_pixels * 100 for cls, count in class_pixel_counts.items()}

    classes = list(class_percentages.keys())
    percentages = list(class_percentages.values())

    return classes, percentages



def get_predictions_result(w,h,y_pred_argmax):

    mask = reconstruct_image_from_patches(y_pred_argmax, (w,h), (256,256))
    mask = convert_2D_label_to_rgb(mask)
    mask1_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

    return mask1_rgb


def binary_changes_detection(mask1,mask2):

    value_to_color = {
      4: (60, 16, 152),  # Building
      1: (254, 221, 58),  # Vegetation
      2: (226, 169, 41),  # Water
      3: (110, 193, 228),  # Road
      0: (132, 41, 246),  # Land
      5: (0, 255, 35),  # Cultivated_Field
      6: (255, 0, 0),  # Uncultivated_Field
      7: (0, 0, 255)  # Football_field
    }

    mask = np.abs(mask2 - mask1)

    # Créez un tableau vide pour stocker les couleurs
    colorized_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    # Remplacez les valeurs dans mask2 par les couleurs correspondantes
    for value, color in value_to_color.items():
        if value != 0:
          colorized_mask[mask == value] = np.array([255, 255, 255])
        else:
          colorized_mask[mask == value] = np.array([0, 0, 0])

    return colorized_mask

import numpy as np

def binary_changes_detection_superposed(mask1, mask2, real_image):
    value_to_color = {
        4: (60, 16, 152),  # Building
        1: (254, 221, 58),  # Vegetation
        2: (226, 169, 41),  # Water
        3: (110, 193, 228),  # Road
        0: (132, 41, 246),  # Land
        5: (0, 255, 35),  # Cultivated_Field
        6: (255, 0, 0),  # Uncultivated_Field
        7: (0, 0, 255)  # Football_field
    }

    mask = np.abs(mask2 - mask1)

    # Créez un tableau vide pour stocker les couleurs
    colorized_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    # Remplacez les valeurs dans mask2 par les couleurs correspondantes
    for value, color in value_to_color.items():
        if value != 0:
            colorized_mask[mask == value] = np.array([255, 255, 255])

    # Utilisez np.where pour obtenir les indices des pixels blancs dans le masque colorisé
    white_indices = np.where((colorized_mask == [255, 255, 255]).all(axis=2))

    # Remplacez les pixels correspondants dans l'image réelle par la couleur blanche
    overlaid_image = real_image.copy()
    overlaid_image[white_indices[0], white_indices[1], :] = [255, 255, 255]

    return overlaid_image


def multi_changes_detection(mask1, mask2):
    value_to_color = {
      4: (60, 16, 152),  # Building
      1: (254, 221, 58),  # Vegetation
      2: (226, 169, 41),  # Water
      3: (110, 193, 228),  # Road
      0: (132, 41, 246),  # Land
      5: (0, 255, 35),  # Cultivated_Field
      6: (255, 0, 0),  # Uncultivated_Field
      7: (0, 0, 255),  # Football_field
      8: (255,255,255), #Background
    }

    keys_array = np.array(list(value_to_color.keys()))

    mask = np.zeros_like(mask1, dtype=np.uint8)

    for i in range(mask1.shape[0]):
        for j in range(mask1.shape[1]):
            if np.array_equal(mask1[i, j], mask2[i, j]):
                mask[i, j] = mask2[i, j]
            else:
                mask[i, j] = keys_array[-1]  # Assign white color where changes occurred

    colorized_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    for value, color in value_to_color.items():
        colorized_mask[np.all(mask == value, axis=-1)] = color

    return colorized_mask

import segmentation_models as sm
from keras import backend as K

# Define a function to create the custom loss function
def create_custom_loss():
    weights = [1/6]*8

    dice_loss = sm.losses.DiceLoss(class_weights = weights)


    focal_loss = sm.losses.CategoricalFocalLoss()


    total_loss = dice_loss + focal_loss

    return total_loss

def jaccard_coef(y_true, y_pred):

    y_true_flatten = K.flatten(y_true)
    y_pred_flatten = K.flatten(y_pred)
    intersection = K.sum(y_true_flatten * y_pred_flatten)
    final_coef_value = (intersection + 1.0) / (K.sum(y_true_flatten) + K.sum(y_pred_flatten) - intersection + 1.0)
    return final_coef_value

import re

def convertir_coord(coordonnees_str):
    # Expression régulière
    pattern = re.compile(r"(\d+)°(\d+)'([\d.]+)\"([NS])\s+(\d+)°(\d+)'([\d.]+)\"([EW])")

    # Application de l'expression régulière à la chaîne
    resultat = pattern.search(coordonnees_str)

    if resultat:
        degres, minutes, secondes, direction, degres_lon, minutes_lon, secondes_lon, direction_lon = map(str, resultat.groups()[:8])

        # Conversion des coordonnées en décimales
        latitude_decimal = int(degres) + int(minutes) / 60 + float(secondes) / 3600
        longitude_decimal = int(degres_lon) + int(minutes_lon) / 60 + float(secondes_lon) / 3600

        # Appliquer le signe correct en fonction de la direction
        latitude_decimal = latitude_decimal if direction == 'N' else -latitude_decimal
        longitude_decimal = longitude_decimal if direction_lon == 'E' else -longitude_decimal

        # Retourner les coordonnées sous forme de liste
        return [
            [round(longitude_decimal - 0.05, 4), round(latitude_decimal + 0.05, 4)],
            [round(longitude_decimal - 0.15, 4), round(latitude_decimal + 0.05, 4)],
            [round(longitude_decimal - 0.15, 4), round(latitude_decimal + 0.15, 4)],
            [round(longitude_decimal - 0.05, 4), round(latitude_decimal + 0.15, 4)],
        ]
    else:
        # Retourner une liste vide si aucune correspondance n'est trouvée
        return []


import folium
import ee

def add_ee_layer(map, ee_object, vis_params, name):
    map_id_dict = ee.Image(ee_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
    ).add_to(map)

import json
from google.oauth2.credentials import Credentials

def initialize():
    # Emplacement du fichier de configuration
    credentials_file_path = 'application_default_credentials.json'

    # Charger les informations d'authentification depuis le fichier
    with open(credentials_file_path, 'r') as file:
        credentials_data = json.load(file)

    # Créer une instance de Credentials
    credentials = Credentials.from_authorized_user_info(credentials_data)

    # Utilisez les informations d'authentification dans votre application
    ee.Initialize(credentials=credentials)