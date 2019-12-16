{% load static %} 
<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
		<script src="{% static 'js/jquery-3.1.1.min.js' %}"></script>  
    	<script src="{% static 'js/bootstrap.min.js' %}"></script>
    	<script src="{% static 'js/plotly-latest.min.js' %}"></script>
	<script src="{% static 'js/plotly-latest.min.js' %}"></script>
	<style>
	canvas{
		-moz-user-select: none;
		-webkit-user-select: none;
		-ms-user-select: none;
	}
	</style>
</head>

<body>
  <div id="myDiv" style="height: 620px;"></div>
	<script type="text/javascript">
		var busroute1 = {
  x: [50,60,55,100,80,75,50],
  y: [50,80,100,80,40,70,50],
  mode: 'lines+markers',
  name: 'BUS DEPOTS',
  text: ['B1', 'B2','B3', 'B4','B5', 'B6','B7', 'B8','B9', 'B10','B11', 'B12','B13', 'B14','B15', 'B16','B17', 'B18','B19', 'B20', 'B21', 'B22'],
  marker: {
    color: 'rgb(164, 194, 244)',
    size: 12,
    line: {
      color: 'white',
      dash: 'dot',
      width: 0.5
    }
  },
  type: 'scatter'

};
var busroute2 = {
  x: [50,70,45,0,20,25,50,40,0,25,50],
  y: [50,20,10,20,60,30,50,80,80,70,50],
  mode: 'lines+markers',
  name: 'BUS DEPOTS',
  text: ['B1', 'B2','B3', 'B4','B5', 'B6','B7', 'B8','B9', 'B10','B11', 'B12','B13', 'B14','B15', 'B16','B17', 'B18','B19', 'B20', 'B21', 'B22'],
  marker: {
    color: 'rgb(164, 194, 0)',
    size: 12,
    line: {
      color: 'white',
      dash: 'dot',
      width: 0.5
    }
  },
  type: 'scatter'

};
var school = {
  x: [50],
  y: [50],
  mode: 'markers',
  name: 'SCHOOL',
  text: ['school'],
  marker: {
    color: 'rgb(255,165,0)',
    size: 50
  }
};


var data = [ busroute1,school ,busroute2];

var layout = {
  title: 'BUS ROUTES SIMULATION',
  xaxis: {
    title: 'x axis distance in km',
    showline: false,
	"gridcolor": "rgb(0,0,0)"
  },
  yaxis: {
    title: 'y axis distance in km',
    showline: false,
    "gridcolor": "rgb(0,0,0	)"
  },
  images: [
      {
        "source": "{% static 'image/bus.png' %}",
        "xref": "x",
        "yref": "y",
        "x": 40,
        "y": 25,
        "sizex": 10,
        "sizey": 20,
        "sizing": "stretch",
        "opacity": 1,
        "layer": "above"
      },
      
    ]

};

Plotly.newPlot('myDiv', data, layout, {showSendToCloud: true} );
	</script>
	

		<!-- sdjkfdddddd
		<p id="demo"></p>
    	<button onclick="stopSimulation()">Stop Timer</button> -->
		<script type="text/javascript">
		    var myVar;
		    function getUpdate(){
		    	$.ajax({
	              url: "/simulator/",
	              data: {'csrfmiddlewaretoken':'{{csrf_token}}','updates':'ifUIisusedforupdatepassdatafromhere'},
	              cache: false,
	              type: "POST",
	              success: function(response) {
	                console.log("SUCCESS");
	                console.log(response);
	                  
	               },
	              error: function(xhr) {
	                console.log("FAILED");
	                console.log(xhr);
	              }
	            });
		    }    
		    function startSimulation(){
		        var d = new Date();
		        var t = d.toLocaleTimeString();
		        $("#demo").html(t); // display data on the page
		        var data =getUpdate();
		    }
		    function stopSimulation(){
		        clearInterval(myVar); // stop the simualtion
		    }
		    $(document).ready(function(){
		        // startSimulation();
		        // myVar = setInterval("startSimulation()", 1000);
		    });
		</script>	
	</body>
</html>
