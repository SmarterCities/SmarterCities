<div id = "application">

    <h1> 1. Choose a model: </h1>
    <div id = 'buttons'>
		<button onclick="input('SmarterHousing')" type="button">SmarterHousing</button>
		<button onclick="input('ExampleModel')" type="button">ExampleModel</button>
		<button onclick="input('Affordable')" type="button">Affordable</button>
    </div>
    <script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
	<script>
	function input(model) {
        $.get("http://smartercities-api.mybluemix.net/input",{}).then(function(r){
            var input_box = document.getElementById('input');
            	input_box.innerHTML=r;
        })

        //$.getScript("http://smartercities-api.mybluemix.net/input/"+model)
	}
	</script>
	
	<h1> 2. Set the parameters you want to use: </h1>
	<div id = 'input'>

		<script>
			var test = 10;

			d3.json("EXAMPLE.json", function(error, data){
				var sliderArray = [];
				(data.sliders).forEach(function(x){
					sliderArray.push(x);
					
				
				});

				console.log(sliderArray);

    	d3.select("div#input").selectAll("div")
					.data(sliderArray)
					.enter().append("div")
	    		.attr("height", "20px")
				.attr("class", "sliders")
				.attr("z-index", "99999")
				.call(d3.slider().on("slide", function(evt, value) {
						d3.select('#inputvalue').text(value);
			}));
		
		});

			

		</script>
	</div>
	<div id="inputvalue">
	</div>
	<div>
     <h1> 3. Run the model: </h1>
	<button onclick="output()" type="button">Run</button>
</div>
<div>
     <h1> 4. Review the output: </h1>
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
	<script>
	function output() {
        	var map = document.getElementById('map')
		var marker = L.marker([40.706363, -74.009096]).addTo(map);
      	//marker.bindPopup("<b>I'm a marker!</b><br>");
	}
	</script>
</div>

</div>