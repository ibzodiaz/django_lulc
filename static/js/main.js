document.addEventListener('DOMContentLoaded', function () {

const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});




// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');
const modeDarkUp  = document.querySelector('.box-container-up');
const modeDarkDown  = document.querySelector('.box-container-down');

const Land = document.querySelector('.Land-s');
const Vegetation = document.querySelector('.Vegetation-s');
const Water = document.querySelector('.Water-s');
const Road = document.querySelector('.Road-s');
const Foot = document.querySelector('.Foot-s');
const Cultivated = document.querySelector('.Cultivated-s');
const Uncultivated = document.querySelector('.Uncultivated-s');
const Building = document.querySelector('.Building-s');

const tableCustom = document.querySelector('.table-custom');
const colorCustom = document.querySelector('.color-custom');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
		modeDarkUp.style.backgroundColor = '#0C0C1E';
		modeDarkDown.style.backgroundColor = '#0C0C1E';
		tableCustom.style.backgroundColor = '#0C0C1E';
		colorCustom.style.color = '#FFFFFF';

		Land.style.color ="#FFFFFF";
		Vegetation.style.color ="#FFFFFF";
		Water.style.color ="#FFFFFF";
		Road.style.color ="#FFFFFF";
		Foot.style.color ="#FFFFFF";
		Cultivated.style.color ="#FFFFFF";
		Uncultivated.style.color ="#FFFFFF";
		Building.style.color ="#FFFFFF";
		
	} else {
		document.body.classList.remove('dark');
		modeDarkUp.style.backgroundColor = '';
		modeDarkDown.style.backgroundColor = '';
		tableCustom.style.backgroundColor = '';
		colorCustom.style.color = '';

		Land.style.color ="";
		Vegetation.style.color ="";
		Water.style.color ="";
		Road.style.color ="";
		Foot.style.color ="";
		Cultivated.style.color ="";
		Uncultivated.style.color ="";
		Building.style.color ="";
	}
})

var buildingElement = document.getElementById("building");
var landElement = document.getElementById("land");
var roadElement = document.getElementById("road");
var vegetationElement = document.getElementById("vegetation");
var waterElement = document.getElementById("water");
var cultivatedElement = document.getElementById("cultivated");
var uncultivatedElement = document.getElementById("uncultivated");
var footballElement = document.getElementById("football");

// Accéder à la valeur de l'attribut data-land en utilisant dataset
var dataBuildingValue = buildingElement.dataset.building;
var dataLandValue = landElement.dataset.land;
var dataRoadValue = roadElement.dataset.road;
var dataVegetationValue = vegetationElement.dataset.vegetation;
var dataWaterValue = waterElement.dataset.water;
var dataCultivatedValue = cultivatedElement.dataset.cultivated;
var dataUncultivatedValue = uncultivatedElement.dataset.uncultivated;
var dataFootballValue = footballElement.dataset.football;


const ctx = document.getElementById('myChart');

new Chart(ctx, {
type: 'pie',
data: {
	labels: ['Bâtiments', 'Terre', 'Routes', 'Végétation', 'Eau', 'Champs cultivés','Champs non cultivés', 'Terrain de football'],
	datasets: [{
	label: 'Taux',
	data: [
			dataBuildingValue,
			dataLandValue,
			dataRoadValue, 
			dataVegetationValue, 
			dataWaterValue, 
			dataCultivatedValue, 
			dataUncultivatedValue,
			dataFootballValue
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


});

