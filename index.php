<!doctype html>

<html lang="en">

<head>
  <meta charset="utf-8">
  <title>SmarterCities</title>
  <meta name="description" content="Smarter Cities">
  <meta name="author" content="Lucio Tolentino">
  <link rel="stylesheet" type="text/css" href="style.css" media="screen" />
  <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
  <link href='http://fonts.googleapis.com/css?family=Playfair+Display' rel='stylesheet' type='text/css'>
</head>

<body class="body">

    <div id="main">
    
    <h1>SmarterCities</h1>

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

    <div id = 'buttons'>
    <button type="button">SmarterHousing</button>
    <button type="button">ExampleModel</button>
    <button type="button">Affordable</button>
    </div>

    </div> <!-- end #main -->

</body>
</html>