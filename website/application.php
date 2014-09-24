<div id = "application">

    <div id = 'buttons'>
		<button onclick="myFunction('SmarterHousing')" type="button">SmarterHousing</button>
		<button onclick="myFunction('ExampleModel')" type="button">ExampleModel</button>
		<button onclick="myFunction('Affordable')" type="button">Affordable</button>
    </div>
	<script>
	function myFunction(model) {
		//var xhr = new XMLHttpRequest();
		//xhr.open("POST", "http://smartercities-api.mybluemix.net/input/"+model, false);
		//xhr.send();
		
		var input_box = document.getElementById('input')
		input_box.innerHTML=model
	}
	</script>
	
	
	<div id = 'input'>
	</div>

	<div id = 'map'>
	</div>
	<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>  
    <script>
  	var map = L.map('map').setView([40.706363, -74.009096], 11);
  		L.tileLayer('https://{s}.tiles.mapbox.com/v3/seanluciotolentino.jhknj4m5/{z}/{x}/{y}.png', {
		    attribution: 'Attribution goes here'
		}).addTo(map);
    </script>


</div>