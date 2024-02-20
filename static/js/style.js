document.addEventListener('DOMContentLoaded', function () {

var buildingElement1 = document.getElementById("building1");
var landElement1 = document.getElementById("land1");
var roadElement1 = document.getElementById("road1");
var vegetationElement1 = document.getElementById("vegetation1");
var waterElement1 = document.getElementById("water1");
var cultivatedElement1 = document.getElementById("cultivated1");
var uncultivatedElement1 = document.getElementById("uncultivated1");
var footballElement1 = document.getElementById("football1");

// Accéder à la valeur de l'attribut data-land en utilisant dataset
var dataBuildingValue1 = buildingElement1.dataset.building1;
var dataLandValue1 = landElement1.dataset.land1;
var dataRoadValue1 = roadElement1.dataset.road1;
var dataVegetationValue1 = vegetationElement1.dataset.vegetation1;
var dataWaterValue1 = waterElement1.dataset.water1;
var dataCultivatedValue1 = cultivatedElement1.dataset.cultivated1;
var dataUncultivatedValue1 = uncultivatedElement1.dataset.uncultivated1;
var dataFootballValue1 = footballElement1.dataset.football1;


var buildingElement2 = document.getElementById("building2");
var landElement2 = document.getElementById("land2");
var roadElement2 = document.getElementById("road2");
var vegetationElement2 = document.getElementById("vegetation2");
var waterElement2 = document.getElementById("water2");
var cultivatedElement2 = document.getElementById("cultivated2");
var uncultivatedElement2 = document.getElementById("uncultivated2");
var footballElement2 = document.getElementById("football2");

// Accéder à la valeur de l'attribut data-land en utilisant dataset
var dataBuildingValue2 = buildingElement2.dataset.building2;
var dataLandValue2 = landElement2.dataset.land2;
var dataRoadValue2 = roadElement2.dataset.road2;
var dataVegetationValue2 = vegetationElement2.dataset.vegetation2;
var dataWaterValue2 = waterElement2.dataset.water2;
var dataCultivatedValue2 = cultivatedElement2.dataset.cultivated2;
var dataUncultivatedValue2 = uncultivatedElement2.dataset.uncultivated2;
var dataFootballValue2 = footballElement2.dataset.football2;


const ctx3 = document.getElementById('myChart3');

new Chart(ctx3, {
type: 'pie',
data: {
	labels: ['Bâtiments', 'Terre', 'Routes', 'Végétation', 'Eau', 'Champs cultivés','Champs non cultivés', 'Terrain de football'],
	datasets: [{
	label: 'Taux de différence',
	data: [
			dataBuildingValue2-dataBuildingValue1,
			dataLandValue2-dataLandValue1,
			dataRoadValue2-dataRoadValue1, 
			dataVegetationValue2-dataVegetationValue1, 
			dataWaterValue2-dataWaterValue1, 
			dataCultivatedValue2-dataCultivatedValue1, 
			dataUncultivatedValue2-dataUncultivatedValue1,
			dataFootballValue2-dataFootballValue1
		],
	backgroundColor: [
		'rgb(60, 16, 152)',  // Violet (Building)
		'rgb(132, 41, 246)', // Mauve (Land)
		'rgb(110, 193, 228)',  // Bleu clair (Road)
		'rgb(254, 221, 58)', // Jaune (Vegetation)
		'rgb(226, 169, 41)', // Jaune foncé (Water)
		'rgb(0, 255, 35)',  // Vert (Cultivated)
		'rgb(255, 0, 0)',  // Rouge (Uncultivated)
		'rgb(0, 0, 255)'  // Bleu (Football)
	],
	borderWidth: 1
	}]
},
options: {
	scales: {
	y: {
		beginAtZero: true
	}
	}
}
});


// Données pour les deux courbes
var data = {
	labels: ['Bâtiments', 'Terre', 'Routes', 'Végétation', 'Eau', 'Champs cultivés','Champs non cultivés', 'Terrain de football'],
	datasets: [
		{
			label: 'Passé',
			borderColor: 'rgb(54, 32, 189)',
			data: [
				dataBuildingValue1,
				dataLandValue1,
				dataRoadValue1, 
				dataVegetationValue1, 
				dataWaterValue1, 
				dataCultivatedValue1, 
				dataUncultivatedValue1,
				dataFootballValue1
			],
			fill: false,
			backgroundColor: 'rgb(54, 32, 189)'
		},
		{
			label: 'Actuelle',
			borderColor: 'rgb(30,25,64)',
			data: [
				dataBuildingValue2,
				dataLandValue2,
				dataRoadValue2, 
				dataVegetationValue2, 
				dataWaterValue2, 
				dataCultivatedValue2, 
				dataUncultivatedValue2,
				dataFootballValue2
			],
			fill: false, // Ne pas remplir la zone sous la courbe
			backgroundColor: 'rgb(30,25,64)'
		},
	],
	borderWidth: 1
};

// Options du graphique
var options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            type: 'category',
        },
        y: {
            beginAtZero: true,
        },
    },
    legend: {
        labels: {
            // Utilisez le même code de couleur que borderColor
            color: 'rgba(255, 99, 132, 1)',
        },
    },
};

// Créer le graphique
var hist = document.getElementById('hist').getContext('2d');
new Chart(hist, {
	type: 'bar',
	data: data,
	options: options,
});

//['Bâtiments', 'Terre', 'Routes', 'Végétation', 'Eau', 'Champs cultivés','Champs non cultivés', 'Terrain de football']

});