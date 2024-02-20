import base64
from django.shortcuts import render, HttpResponse
import cv2
import numpy as np
from . import functions

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import custom_object_scope

import ee
import json
from google.oauth2.credentials import Credentials
import folium
from branca.element import Figure

import gc


def home_view(request):

    if request.method == 'POST' and 'submit' in request.POST:
        if request.FILES.get('file'):
            with custom_object_scope({'dice_loss_plus_focal_loss': functions.create_custom_loss,'jaccard_coef':functions.jaccard_coef}):
                model = load_model('fine_tuned_best_inception_resnetv2_unet_model.h5')

            
            uploaded_file = request.FILES['file']
            image1 = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
            

            image_dataset1 = functions.get_image_dataset(image1)[0]
            patches_img1 = functions.get_image_dataset(image1)[1]
            h1 = functions.get_image_dataset(image1)[2]
            w1 = functions.get_image_dataset(image1)[3]

            #img1 = unpatchify(patches_img1,image1.shape)

            image_dataset1 = np.array(image_dataset1)
            y_pred1 = model.predict(image_dataset1)
            y_pred_argmax1 = np.argmax(y_pred1, axis=3)

            
            mask1 = functions.get_predictions_result(w1,h1,y_pred_argmax1)
            repartition = functions.mask_repartition(mask1)
            classes = repartition[0]
            percentages = repartition[1]

            # convertir l'image en jpg
            _, jpeg = cv2.imencode('.jpg', image1, [cv2.IMWRITE_JPEG_QUALITY, 90])

            image_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')


            _, jpeg = cv2.imencode('.jpg', mask1, [cv2.IMWRITE_JPEG_QUALITY, 90])
            colored_mask_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            context = {
                    'image_base64': image_base64, 
                    'colored_mask_base64': colored_mask_base64, 
                    'Building' : percentages[0],
                    'Land': percentages[1],
                    'Road': percentages[2],
                    'Vegetation': percentages[3],
                    'Water': percentages[4],
                    'Cultivated_field': percentages[5],
                    'Uncultivated_field':  percentages[6],
                    'Football_field': percentages[7],
                    'classes':classes,
                    'percentages':percentages
                    }
            
            
            return render(request, 'home.html', context)
        else:
            message = "Veuillez insérer une image satellite!"
            context = {'message': message}
            return render(request, 'home.html', context)
        
    return render(request, 'home.html')

import math

def detection(request):
    if request.method == 'POST' and 'submit' in request.POST:
        if request.FILES.get('file1') and request.FILES.get('file2'):
            with custom_object_scope({'dice_loss_plus_focal_loss': functions.create_custom_loss,'jaccard_coef':functions.jaccard_coef}):
                model = load_model('fine_tuned_best_inception_resnetv2_unet_model.h5')

            
            uploaded_file1 = request.FILES['file1']
            image1 = cv2.imdecode(np.fromstring(uploaded_file1.read(), np.uint8), cv2.IMREAD_COLOR)
            height1, width1 = image1.shape[:2]
            
            uploaded_file2 = request.FILES['file2']
            image2 = cv2.imdecode(np.fromstring(uploaded_file2.read(), np.uint8), cv2.IMREAD_COLOR)
            height2, width2 = image2.shape[:2]

            image_dataset1 = functions.get_image_dataset(image1)[0]
            patches_img1 = functions.get_image_dataset(image1)[1]
            h1 = functions.get_image_dataset(image1)[2]
            w1 = functions.get_image_dataset(image1)[3]

            image_dataset2 = functions.get_image_dataset(image2)[0]
            patches_img2 = functions.get_image_dataset(image2)[1]
            h2 = functions.get_image_dataset(image2)[2]
            w2 = functions.get_image_dataset(image2)[3]

            #img1 = unpatchify(patches_img1,image1.shape)

            image_dataset1 = np.array(image_dataset1)
            y_pred1 = model.predict(image_dataset1)
            y_pred_argmax1 = np.argmax(y_pred1, axis=3)

            gc.collect()

            image_dataset2 = np.array(image_dataset2)
            y_pred2 = model.predict(image_dataset2)
            y_pred_argmax2 = np.argmax(y_pred2, axis=3)

            gc.collect()
            
            mask1 = functions.reconstruct_image_from_patches(y_pred_argmax1, (w1,h1), (256,256))
            mask2 = functions.reconstruct_image_from_patches(y_pred_argmax2, (w2,h2), (256,256))

            repartition1 = functions.mask_repartition(functions.get_predictions_result(w1,h1,y_pred_argmax1))
            classes1 = repartition1[0]
            percentages1 = repartition1[1]

            repartition2 = functions.mask_repartition(functions.get_predictions_result(w2,h2,y_pred_argmax2))
            classes2 = repartition2[0]
            percentages2 = repartition2[1]
            

            result = functions.binary_changes_detection_superposed(mask1, mask2, image2)
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

            _, jpeg = cv2.imencode('.jpg', result, [cv2.IMWRITE_JPEG_QUALITY, 90])
            areas_changed = base64.b64encode(jpeg.tobytes()).decode('utf-8')

            operation = request.POST.get('operations', '')
            epsilon = 0.01

            diff1 = 0
            diff2 = 0
            diff3 = 0
            diff4 = 0
            diff5 = 0
            diff6 = 0
            diff7 = 0
            diff8 = 0

            #if operation == 'A':
            diff1 = percentages2[0] - percentages1[0]
            diff2 = percentages2[1] - percentages1[1]
            diff3 = percentages2[2] - percentages1[2]
            diff4 = percentages2[3] - percentages1[3]
            diff5 = percentages2[4] - percentages1[4]
            diff6 = percentages2[5] - percentages1[5]
            diff7 = percentages2[6] - percentages1[6]
            diff8 = percentages2[7] - percentages1[7]

            """elif operation == 'R':
                diff1 = ((percentages2[0] - percentages1[0]) / (percentages1[0] + epsilon)) * 100
                diff2 = ((percentages2[1] - percentages1[1]) / (percentages1[1] + epsilon)) * 100
                diff3 = ((percentages2[2] - percentages1[2]) / (percentages1[2] + epsilon)) * 100
                diff4 = ((percentages2[3] - percentages1[3]) / (percentages1[3] + epsilon)) * 100
                diff5 = ((percentages2[4] - percentages1[4]) / (percentages1[4] + epsilon)) * 100
                diff6 = ((percentages2[5] - percentages1[5]) / (percentages1[5] + epsilon)) * 100
                diff7 = ((percentages2[6] - percentages1[6]) / (percentages1[6] + epsilon)) * 100
                diff8 = ((percentages2[7] - percentages1[7]) / (percentages1[7] + epsilon)) * 100

            elif operation == 'L':

                diff1 = math.log((percentages2[0] + epsilon) / (percentages1[0] + epsilon))
                diff2 = math.log((percentages2[1] + epsilon) / (percentages1[1] + epsilon))
                diff3 = math.log((percentages2[2] + epsilon) / (percentages1[2] + epsilon))
                diff4 = math.log((percentages2[3] + epsilon) / (percentages1[3] + epsilon))
                diff5 = math.log((percentages2[4] + epsilon) / (percentages1[4] + epsilon))
                diff6 = math.log((percentages2[5] + epsilon) / (percentages1[5] + epsilon))
                diff7 = math.log((percentages2[6] + epsilon) / (percentages1[6] + epsilon))
                diff8 = math.log((percentages2[7] + epsilon) / (percentages1[7] + epsilon))
            """
            
            context = {
                        'areas_changed': areas_changed, 
                        'Building1' : percentages1[0],
                        'Land1': percentages1[1],
                        'Road1': percentages1[2],
                        'Vegetation1': percentages1[3],
                        'Water1': percentages1[4],
                        'Cultivated_field1': percentages1[5],
                        'Uncultivated_field1':  percentages1[6],
                        'Football_field1': percentages1[7],
                        'classes1':classes1,
                        'percentages1':percentages1,
                        'Building2' : percentages2[0],
                        'Land2': percentages2[1],
                        'Road2': percentages2[2],
                        'Vegetation2': percentages2[3],
                        'Water2': percentages2[4],
                        'Cultivated_field2': percentages2[5],
                        'Uncultivated_field2':  percentages2[6],
                        'Football_field2': percentages2[7],
                        'classes2':classes2,
                        'percentages2':percentages2,
                        'diff1': diff1,
                        'diff2': diff2,
                        'diff3': diff3,
                        'diff4': diff4,
                        'diff5': diff5,
                        'diff6': diff6,
                        'diff7': diff7,
                        'diff8': diff8
                    }
            
            
            return render(request, 'detection.html', context)
        else:
            message = "Veuillez insérer deux images satellites!"
            context = {'message': message}
            return render(request, 'detection.html', context)
    return render(request, 'detection.html')

import ee
import folium
from django.shortcuts import render
import re
import requests

functions.initialize()


def map(request):
    try:
 
        # Authenticate to Earth Engine
        ee.Initialize()

        # Define the geometry
        geom = ee.Geometry.Polygon([
            [-15.7, 16.4667],  # Point 1
            [-15.8, 16.4667],  # Point 2
            [-15.8, 16.5667],  # Point 3
            [-15.7, 16.5667],
        ])

        Bands = ['B4', 'B3', 'B2','pixel_qa']

        day1, month1, year1 = '01', '01', '2013'
        day2, month2, year2 = '31', '12', '2013'

        start = f'{year1}-{month1}-{day1}'
        end = f'{year2}-{month2}-{day2}'

        context = {}

        Landsat = 'LANDSAT/LC08/C01/T1_SR'

        dataset = ee.ImageCollection(Landsat) \
                .filterBounds(geom) \
                .filterDate(start, end) \
                .select(Bands)
       
        image = dataset.first()

        band_names = image.bandNames()
        print("Noms des bandes :", band_names.getInfo())
        
        # Sélectionnez les bits du pixel QA qui correspondent aux nuages.
        cloud_mask = 1 << 3  
        cloud_mask = image.select('pixel_qa').bitwiseAnd(cloud_mask).eq(0)
        image = image.updateMask(cloud_mask)

        # Compute the median
        reduction = dataset.median()

        # Compute min and max values for visualization
        stats = reduction.reduceRegion(ee.Reducer.minMax(), geom, 100)
        stat_dict = stats.getInfo()

        # Create a folium map centered around the geometry
        center = [geom.centroid().coordinates().get(1).getInfo(), geom.centroid().coordinates().get(0).getInfo()]
        m = folium.Map(location=center, zoom_start=10, control_scale=True)

        vue_satellite = request.POST.get('vue_satellite', False)  # Récupérer la valeur de la case à cocher

        # Ajoutez une couche supplémentaire pour la vue satellite si l'option est activée
        if request.method == 'POST' and 'submit_view' in request.POST:
            if vue_satellite:
                google_satellite = folium.raster_layers.TileLayer(
                    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                    attr='Google Satellite',
                    name='Google Satellite',
                    overlay=True,
                    control=True
                )
                google_satellite.add_to(m)

        vis_params = {
                        'bands': Bands[:3],
                        'min': [stat_dict['B4_min'], stat_dict['B3_min'], stat_dict['B2_min']],
                        'max': [stat_dict['B4_max'], stat_dict['B3_max'], stat_dict['B2_max']],
                        'gamma': 1.4
                    }
        functions.add_ee_layer(m, reduction, vis_params, 'Median Composite')

        google_earth_url = f"https://earth.google.com/web/"

        if request.method == 'POST' and 'submit' in request.POST:
            day1 = request.POST.get('day1', '')
            month1 = request.POST.get('month1', '')
            year1 = request.POST.get('year1', '')

            day2 = request.POST.get('day2', '')
            month2 = request.POST.get('month2', '')
            year2 = request.POST.get('year2', '')

            resolution_width = 1050
            resolution_height = 632

            resolution = request.POST.get('resolution','')

            if year1 <= year2 or month1 < month2:
                coord = request.POST.get('coord', '')

                # Expression régulière pour extraire les dimensions
                pattern = re.compile(r"(\d+)x(\d+)")

                # Application de l'expression régulière à la chaîne de résolution
                match = pattern.match(resolution)

                # Vérification si la correspondance est trouvée
                if match:
                    # Extraction des valeurs de largeur et de hauteur
                    resolution_width = int(match.group(1))
                    resolution_height = int(match.group(2))

                    # Utilisation des valeurs
                    print("Largeur :", resolution_width)
                    print("Hauteur :", resolution_height)

                if coord :
                    
                    if len(functions.convertir_coord(coord)) != 0:
                        polygon_coords = functions.convertir_coord(coord)
                    else:
                        message = f'Le format de coordonnées données n\'est pas valide!<br>Exemple de format valide 14°43\'19"N 17°28\'20"W <br><a href="{google_earth_url}">Allez ver GEP pour récupérer les coordonnées de la zone d\'intérêt</a>'
                        context = {'error': message}
                        return render(request,'map.html',context)
                else:
                    # Récupérer les coordonnées actuelles du centre de la carte
                    center_lat = m.location[0]
                    center_lon = m.location[1]

                    # Définir la taille de la région d'intérêt en degrés (ajustez selon vos besoins)
                    roi_size = 0.05  # par exemple, une région de 0.1 degré autour du centre

                    # Définir les sommets du polygone autour du centre de la carte
                    polygon_coords = [
                        [center_lon - roi_size / 2, center_lat - roi_size / 2],
                        [center_lon + roi_size / 2, center_lat - roi_size / 2],
                        [center_lon + roi_size / 2, center_lat + roi_size / 2],
                        [center_lon - roi_size / 2, center_lat + roi_size / 2]
                    ]

                    google_earth_url = f"https://earth.google.com/web/@{center_lat},{center_lon}"

                print(polygon_coords)
                
                geom = ee.Geometry.Polygon(polygon_coords)

                if day1 and month1 and year1 and day2 and month2 and year2:
                    start = f"{year1}-{month1.zfill(2)}-{day1.zfill(2)}"
                    end = f"{year2}-{month2.zfill(2)}-{day2.zfill(2)}"

                    dataset = ee.ImageCollection(Landsat) \
                    .filterBounds(geom) \
                    .filterDate(start, end) \
                    .select(Bands)
                    
                    image_count = dataset.size().getInfo()
    
                    if image_count > 0:
                        # Select the first image in the collection
                        image = dataset.first()
                        cloud_mask = 1 << 3  
                        cloud_mask = image.select('pixel_qa').bitwiseAnd(cloud_mask).eq(0)
                        image = image.updateMask(cloud_mask)

                        # Compute the median
                        reduction = dataset.median()

                        # Compute min and max values for visualization
                        stats = reduction.reduceRegion(ee.Reducer.minMax(), geom, 100)
                        stat_dict = stats.getInfo()

                        # Create a folium map centered around the geometry
                        center = [geom.centroid().coordinates().get(1).getInfo(), geom.centroid().coordinates().get(0).getInfo()]
                        m = folium.Map(location=center, zoom_start=10, control_scale=True)

                        if all(band in stat_dict for band in Bands):
                            # Définissez les paramètres de visualisation en fonction des statistiques
                            vis_params = {
                                            'bands': Bands[:3],
                                            'min': [stat_dict['B4_min'], stat_dict['B3_min'], stat_dict['B2_min']],
                                            'max': [stat_dict['B4_max'], stat_dict['B3_max'], stat_dict['B2_max']],
                                            'gamma': 1.4
                                        }
                        else:
                            # Gérez le cas où les clés nécessaires ne sont pas présentes
                            vis_params = {
                                'bands': Bands[:3],
                                'min': 0,
                                'max': 3000,
                                'gamma': 1.4
                            }
                            print("Les statistiques pour les bandes B4, B3, B2 ne sont pas disponibles. Paramètres par défaut utilisés.")
                        functions.add_ee_layer(m, reduction, vis_params, 'Median Composite')

                    else:
                        message = "Aucune image Landsat disponible pour la région et la période spécifiées."
                        print(message)
                        context = {
                                    'folium_map': m._repr_html_(),
                                    'google_earth_url': google_earth_url,
                                    'error':message
                                    }
                        return render(request, 'map.html', context)
                    
                else:
                    # Handle invalid or empty date inputs
                    # You might want to redirect the user to the form with an error message
                    return render(request, 'map.html', {'error': 'Les entrées sont invalides!'})
                
                functions.add_ee_layer(m, reduction, vis_params, 'Median Composite')

                # Get the download URL for the selected image with specified resolution
                url = image.reproject('EPSG:4326', None, 30).getThumbURL({
                    'bands': vis_params['bands'], 
                    'min': vis_params['min'], 
                    'max': vis_params['max'], 
                    'gamma': vis_params['gamma'], 
                    'dimensions': f'{resolution_width}x{resolution_height}'
                })

                context = {
                        'folium_map': m._repr_html_(), 
                        'download_url': url,
                        'google_earth_url': google_earth_url,
                        'days': list(range(1,32)),
                        'months': list(range(1,13)),
                        'years': list(range(1997,2024)),
                        'years2':list(range(1998,2024)),
                        'day_1': day1,
                        'month_1': month1,
                        'year_1': year1,
                        'day_2': day2,
                        'month_2': month2,
                        'year_2': year2
                        }

            else:
                message = "L'ordre temporel n'est pas suivi correctement."

                context = {
                        'folium_map': m._repr_html_(),
                        'google_earth_url': google_earth_url,
                        'error':message,
                        'days': list(range(1,32)),
                        'months': list(range(1,13)),
                        'years': list(range(1997,2024)),
                        'years2':list(range(1998,2024)),
                        'day_1': day1,
                        'month_1': month1,
                        'year_1': year1,
                        'day_2': day2,
                        'month_2': month2,
                        'year_2': year2
                        }

            
        else:

            # Pass the folium map and download URL to the template
            context = {
                        'folium_map': m._repr_html_(),
                        'google_earth_url': google_earth_url,
                        'days': list(range(1,32)),
                        'months': list(range(1,13)),
                        'years': list(range(1997,2024)),
                        'years2':list(range(1998,2024)),
                        'day_1': day1,
                        'month_1': month1,
                        'year_1': year1,
                        'day_2': day2,
                        'month_2': month2,
                        'year_2': year2
                        }

        
        

        return render(request, 'map.html', context)
    
    except requests.exceptions.ConnectionError as e:

        context = {'error': f"Erreur de connexion : {e}"}
        return render(request, 'map.html', context)

