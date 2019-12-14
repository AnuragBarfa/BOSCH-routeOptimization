    {% extends 'base.html' %}
    {% load static %}
    {% block title %}Django Ajax Example{% endblock %}
    {% block stylesheet %}
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
    <style type="text/css">
    	#wrapper { position: relative; }
       	#over_map { position: absolute; top: 10px; right: 1%; z-index: 99;  }
    </style>
    <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">

    <style type="text/css">
        body {
            color: #404E67;
            background: #F5F7FA;
        font-family: 'Open Sans', sans-serif;
      }
      .table-wrapper {
        width: 300px;
        background: #f2f2f2; 
        box-shadow: 0 1px 1px rgba(0,0,0,.05);
        }
        .table-title {
            padding-left: 10px;
            padding-bottom: 2px;
            margin: 0 0 10px;
        }
        .table-title h2 {
            margin: 6px 0 0;
            font-size: 22px;
        }
        .table-title .add-new {
            float: right;
        height: 30px;
        font-weight: bold;
        font-size: 12px;
        text-shadow: none;
        min-width: 100px;
        border-radius: 50px;
        line-height: 13px;
        }
      .table-title .add-new i {
        margin-right: 4px;
      }
        table.table {
            table-layout: fixed;
        }
        table.table tr th, table.table tr td {
            border-color: #e9e9e9;
        }
        table.table th i {
            font-size: 13px;
            margin: 0 5px;
            cursor: pointer;
        }
        table.table th:last-child {
            width: 100px;
        }
        table.table td a {
        cursor: pointer;
            display: inline-block;
            margin: 0 2px;
        min-width: 24px;
        }    
      table.table td a.add {
            color: #27C46B;
        }
        table.table td a.edit {
            color: #FFC107;
        }
        table.table td a.delete {
            color: #E34724;
        }
        table.table td i {
            font-size: 19px;
        }
      table.table td a.add i {
            font-size: 24px;
          margin-right: -1px;
            position: relative;
            top: 3px;
        }    
        table.table .form-control {
            height: 32px;
            line-height: 32px;
            box-shadow: none;
            border-radius: 2px;
        }
      table.table .form-control.error {
        border-color: #f50000;
      }
      table.table td .add {
        display: none;
      }
    </style>
    {% endblock %}

    {% block content %}
    	<div class="container-fluid" style="padding: 0px;">
    		<div id="map" style="position:relative;width:100%;height: 800px;float:left;"></div>
    		<div id="over_map" class="pull-right">
          <p>
            <button class="btn btn-primary" aria-expanded="false" onclick="routeopt()">
              Route Optimizer
            </button>
          </p>
    			<div class="table-wrapper">
                <div class="table-title">
                    <div class="row">
                        <div class="col-sm-8">
                            <h2><a data-toggle="collapse" href="#collapseExample1" role="button" aria-expanded="false" aria-controls="collapseExample1">Location</a></h2>
                        </div>
                          <div class="col-sm-4">
                        </div>
                    </div>
                </div>
                <div class="collapse" id="collapseExample1">
                  <div class="card card-body">
                    <div id="loc_searchresult">
                    <table class="table">
                    <thead>
                        <tr>
                            <th>Location</th>
                            <th>P. No.</th>
                            <th><button type="button" class="btn btn-info add-new"><!-- <i class="fa fa-plus"></i> -->Add Loc</button></th>
                          </tr>
                    </thead>
                    <tbody>

                      </tbody>
                </table>
              </div>
                      <i id="hide_no_loc_available">NO LOCATION AVAILABLE</i>
                  </div>
                </div>
                
            </div>

    			
    			<br/>
              <div class="table-wrapper">
                <div class="table-title">
                    <div class="row">
                        <div class="col-sm-8">
                            <h2><a data-toggle="collapse" href="#collapseExample2" role="button" aria-expanded="false" aria-controls="collapseExample2">Buses</a></h2>
                        </div>
                        <div class="col-sm-4">
                            
                        </div>
                    </div>
                </div>
                <div class="collapse" id="collapseExample2">
                  <div class="card card-body">
                    <div id="bus_searchresult">
                    <table class="table">
                    <thead>
                        <tr>
                            <th>Bus No</th>
                            <th>Capacity</th>
                            <th><button type="button" class="btn btn-info add-new" id="bus"><!-- <i class="fa fa-plus"></i> -->Add Bus</button></th>
                        </tr>     
                    </thead>
                    <tbody>
                       </tbody>
                </table>
                <i id="hide_no_bus_available">NO BUS AVAILABLE</i>
                </div>
                <!-- <i id="hide_no_loc_available2">NO BUS AVAILABLE</i> -->
                  </div>
                </div>
                
            </div>



    		</div>
    	</div>
    {% endblock %}

    {% block javascript %}
    <!-- </script> -->
      <script>
          var globa;
          var map;
          var responsestore;
          var request;
          var service;
          var geocoder;
          var storeLocationDetails=new Map();
          var directionsDisplay;
          var directionsService;
          var bounds;
                  var sendtocity=[];
                  var citytostore=[],passengernotostore=[],citylattostore=[],citylngtostore=[];
                  var bustostore=[],capacitytostore=[];
      
            function routeopt(){

              

                   citytostore=[];
                   passengernotostore=[];
                   citylattostore=[];
                   citylngtostore=[];
                   bustostore=[];
                   capacitytostore=[];
      
      
              var data={};
              
              console.log("STORING PSNG NO");
              
              $('#loc_searchresult > table > tbody > tr').each(function() {
                $(this).children('td:nth-child(2)').each(function(){
                  var data = $(this).html();
                console.log(data);
                passengernotostore.push(data);
                })
              });
              
              console.log("STORING BUS NAME");
              
              $('#bus_searchresult > table > tbody > tr').each(function() {
                $(this).children('td:nth-child(1)').each(function(){
                  var data = $(this).html();
                console.log(data);
                bustostore.push(data);
                })
              });
              
              console.log("STORING BUS Capacity");
              
              $('#bus_searchresult > table > tbody > tr').each(function() {
                $(this).children('td:nth-child(2)').each(function(){
                  var data = $(this).html();
                console.log(data);
                capacitytostore.push(data);
                })
              });


             for(key in storeLocationDetails)
                {
                  citytostore.push(key);
                  // text += (key + ' = ' + storeLocationDetails[key].getPosition().lat() + '\n');
                  citylattostore.push(storeLocationDetails[key].getPosition().lat());
                  citylngtostore.push(storeLocationDetails[key].getPosition().lng());
                }

            //////////////////SEND

            // var addressofcity={"CITY":citytostore,"PASSENGER":passengernotostore,"LAT":citylattostore,"LNG":citylngtostore};

            var locations=[];
            var busdetails=[];

            for(var i=0;i<bustostore.length;i++){
              var currLocation={};
              currLocation['busname']=bustostore[i];
              currLocation['buscapacity']=capacitytostore[i];
              busdetails.push(currLocation);
            }

            for(var i=0;i<citytostore.length;i++){
              var currLocation={};
              currLocation['name']=citytostore[i];
              currLocation['count']=passengernotostore[i];
              currLocation['lat']=citylattostore[i];
              currLocation['lng']=citylngtostore[i];
              currLocation['arr']="1";
              currLocation['depa']="1";
              locations.push(currLocation);
            }

            console.log("ADDRESS:");
            // console.log(locations);
              $.ajax({
              url: "route/",
              data: {'csrfmiddlewaretoken':'{{csrf_token}}','locations':JSON.stringify(locations),'busdetails':JSON.stringify(busdetails)},
              cache: false,
              type: "POST",
              success: function(response) {
                console.log("SUCCESS");
                console.log(response);
                  responsestore=response['routes'];
                  console.log(response['routes'][0]['nodes'][0]);
                  for(var i =0;i<response['routes'].length;i++)
                    {  
                      calcRoute(response['routes'][i]);

                      console.log(response['routes'][i]['nodes']);
                    }
                  
                  boundall();
               distancematrix(responsestore,responsestore);

               },
              error: function(xhr) {
                console.log("FAILED");
                console.log(xhr);
              }
              });
                
             return false;
            }

          function initMap() {  

            var myLatLng = {lat: 20, lng: 78};
            directionsService = new google.maps.DirectionsService();
            map = new google.maps.Map(document.getElementById('map'), {
              zoom: 4,
              center: myLatLng,
              // disableDefaultUI: true

            });
            directionsDisplay = new google.maps.DirectionsRenderer({suppressMarkers: true,preserveViewport: true});
            service = new google.maps.DistanceMatrixService;
            directionsDisplay.setMap(map);

            bounds = new google.maps.LatLngBounds();

            calcRoute2(28.7041, 77.884886, 28.334818, 77.94886, 29.34, 76.12)
            calcRoute2(26.7041, 78.884886, 26.334818, 78.94886, 25.3535, 79.123)
            calcRoute2(12.9716, 77.0946, 13.9716, 78.5946, 10.9716, 77.6946)
            // calcRoute2(57.1304, 106.9468, 56.1304, 106.3468, 58.1304, 107.3468)
            var e=new google.maps.LatLng(28.7041, 77.884886);
            bounds.extend(e);
            e=new google.maps.LatLng(28.334818, 77.94886);
            bounds.extend(e);
            e=new google.maps.LatLng(29.34, 76.12);
            bounds.extend(e);
            e=new google.maps.LatLng(26.7041, 78.884886);
            bounds.extend(e);
            e=new google.maps.LatLng(26.334818, 78.94886);
            bounds.extend(e);
            e=new google.maps.LatLng(25.3535, 79.123);
            bounds.extend(e);
            e=new google.maps.LatLng(12.9716, 77.0946);
            bounds.extend(e);
            e=new google.maps.LatLng(13.9716, 78.5946);
            bounds.extend(e);
            e=new google.maps.LatLng(10.9716, 77.6946);
            bounds.extend(e);
            // e=new google.maps.LatLng(57.1304, 106.9468);
            // bounds.extend(e);
            // e=new google.maps.LatLng(56.1304, 106.3468);
            // bounds.extend(e);
            // e=new google.maps.LatLng(58.1304, 107.3468);
            // bounds.extend(e);
            map.fitBounds(bounds);
          }
          function addMarker(location) {
            console.log("in marker");
            marker = new google.maps.Marker({
                position: location,
                map: map
            });
          }
          function calcRoute2(x1,y1,x2,y2,x3,y3) {
                var start = new google.maps.LatLng(x1,y1);
                var end = new google.maps.LatLng(x2,y2);
                var request = {
                    origin: start,
                    waypoints:[],
                    destination: end,
                    travelMode: google.maps.TravelMode.DRIVING
                };
                marker2 = new google.maps.Marker({
                  map: map,
                  position: new google.maps.LatLng(x3,y3),
                });
                // var contentString = '<div id="content">'+
                //       '<div id="siteNotice">'+
                //       '</div>'+
                //       '<h1 id="firstHeading" class="firstHeading">Uluru</h1>'+
                //       '<div id="bodyContent">'+
                //       '<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large ' +
                //       'sandstone rock formation in the southern part of the '+
                //       'Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) '+
                //       'south west of the nearest large town, Alice Springs; 450&#160;km '+
                //       '(280&#160;mi) by road. Kata Tjuta and Uluru are the two major '+
                //       'features of the Uluru - Kata Tjuta National Park. Uluru is '+
                //       'sacred to the Pitjantjatjara and Yankunytjatjara, the '+
                //       'Aboriginal people of the area. It has many springs, waterholes, '+
                //       'rock caves and ancient paintings. Uluru is listed as a World '+
                //       'Heritage Site.</p>'+
                //       '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">'+
                //       'https://en.wikipedia.org/w/index.php?title=Uluru</a> '+
                //       '(last visited June 22, 2009).</p>'+
                //       '</div>'+
                //       '</div>';

                // var infowindow = new google.maps.InfoWindow({
                //   content: contentString
                // });
                // marker2.addListener('click', function() {
                //   infowindow.open(map, marker2);
                // });

                request.waypoints.push({
                  location: marker2.getPosition(),
                  stopover: true
                });
                // directionsService.route(request, function (response, status) {
                //     if (status == google.maps.DirectionsStatus.OK) {
                //         directionsDisplay.setDirections(response);
                //     }
                // });
                var directionsDisplay9 = new google.maps.DirectionsRenderer({
                    suppressMarkers: false,
                    suppressInfoWindows: false,
                    preserveViewport: true
                  });
                  
              //COLOUR
                directionsDisplay9.setOptions({
                  polylineOptions: {
                  strokeColor: 'red'
                  }
                });

                directionsDisplay9.setMap(map);
                var directionsService9 = new google.maps.DirectionsService();
                directionsService9.route(request, function(result, status) {
                  if (status == google.maps.DirectionsStatus.OK) {
                    directionsDisplay9.setDirections(result);
                  }
                });
            }  
          function calcRoute(response) {
            var locations2 = [
            //];
            ['dsv',  122, 127]
          ]; 
          var temp2=[],color=[];
          for(var i=0;i<response['nodes'].length;i++){
            temp2=[];
            color.push(response['color']);
            
            temp2.push(response['nodes'][i]["name"]);      
            temp2.push(response['nodes'][i]["lat"]);
            temp2.push(response['nodes'][i]["lng"]);
            locations2.push(temp2);
          }
          
          console.log("LOC===========");
          console.log(locations2);

          var marker2, i;
          var request = {
          travelMode: google.maps.TravelMode.DRIVING
          };
          for (i = 1; i < locations2.length; i++) {

            marker2 = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(locations2[i][1], locations2[i][2]),
            });

        if (i == 1) {request.origin = marker2.getPosition(); 
           // marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
        }
        else if (i == locations2.length - 1) {request.destination = marker2.getPosition();
        // marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
      }
        else {
          if (!request.waypoints) request.waypoints = [];
            request.waypoints.push({
            location: marker2.getPosition(),
            stopover: true
          });
        }
      }
       var directionsDisplay9 = new google.maps.DirectionsRenderer({
              suppressMarkers: false,
              suppressInfoWindows: true,
              preserveViewport: true
            });
            
      //COLOUR
        directionsDisplay9.setOptions({
        polylineOptions: {
        strokeColor: color[0]
        }
      });

    directionsDisplay9.setMap(map);
      var directionsService9 = new google.maps.DirectionsService();
      directionsService9.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
          directionsDisplay9.setDirections(result);
        }
      });
          


          }
         
  </script>
  <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDmwBs8dSuwg56fTWsbJyMdrvXYU3_Pim4&libraries=places&callback=initMap">
  </script>
  <script type="text/javascript">

    function boundall(){
      

      // for(key in storeLocationDetails)
      //           {
      //               var e = new google.maps.LatLng(storeLocationDetails[key].getPosition().lat(),storeLocationDetails[key].getPosition().lng());
      //               bounds.extend(e);
      //           }
           
      //       console.log(storeLocationDetails);
      //       var store=Object.keys(storeLocationDetails);
      //     for(var i=0;i<store.length;i++){
      //       var e=new google.maps.LatLng(storeLocationDetails[store[i]].getPosition().lat(),storeLocationDetails[store[i]].getPosition().lng());
      //       bounds.extend(e);
      //     }

        
      for(var j=0;j<responsestore.length;j++)
         for(var i=0;i<responsestore[j]['nodes'].length;i++)
         {  
            // console.log("LAT");
            // console.log(responsestore[j]['nodes'][i]["lat"]);
            var e=new google.maps.LatLng(responsestore[j]['nodes'][i]["lat"],responsestore[j]['nodes'][i]["lng"]);
            bounds.extend(e);

         }
            map.fitBounds(bounds);
      }

    function distancematrix(response1,response2){
      // alert("IN");
        var markersArray = [];
        var geocoder = new google.maps.Geocoder();        
        service.getDistanceMatrix({
          origins: response1,//[{},{},]
          destinations: response2,//[{},{}]
          travelMode: 'DRIVING',
          unitSystem: google.maps.UnitSystem.METRIC,
        }, function(response, status) {
          if (status !== 'OK') {
            alert('Error was: ' + status);
          } else {
            var originList = response.originAddresses;
            var destinationList = response.destinationAddresses;
            var outputDiv;
            
            deleteMarkers(markersArray);

            var showGeocodedAddressOnMap = function(asDestination) {
              return function(results, status) {
                if (status === 'OK') {
                  map.fitBounds(bounds.extend(results[0].geometry.location));
                  markersArray.push(new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location,
                  }));
                } else {
                  alert('Geocode was not successful due to: ' + status);
                }
              };
            };

            for (var i = 0; i < originList.length; i++) {
              var results = response.rows[i].elements;
              geocoder.geocode({'address': originList[i]},
                  showGeocodedAddressOnMap(false));
              for (var j = 0; j < results.length; j++) {
                geocoder.geocode({'address': destinationList[j]},
                    showGeocodedAddressOnMap(true));
                outputDiv += originList[i] + "to"  + destinationList[j] +
                    " : " + results[j].distance.text +  "in"  +
                    results[j].duration.text +" ";
              }
            
            console.log(outputDiv);
            }
           
          }
        });

    }

    function deleteMarkers(markersArray) {
        for (var i = 0; i < markersArray.length; i++) {
          markersArray[i].setMap(null);
        }
        markersArray = [];
      }

    function isEmpty( obj ) {
        for ( var name in obj ) {return false;}
        return true;
    }

    function hide_or_show_no_location(){
      if(!isEmpty(storeLocationDetails))
          document.getElementById("hide_no_loc_available").style.display = "none";
      else 
        document.getElementById("hide_no_loc_available").style.display = "block";
    }

    function hide_or_show_no_bus(){
      if(bustostore.length==0)
        document.getElementById("hide_no_bus_available").style.display = "block";
      else
        document.getElementById("hide_no_bus_available").style.display = "none";
    }

    var glob;
    $(document).ready(function()
    {
      document.getElementById("hide_no_loc_available").style.display = "block"; 
      $('[data-toggle="tooltip"]').tooltip();
      var actions = $("table td:last-child").html();
      // Append table with add row form on add new button click
      $(".add-new").click(function(){

        hide_or_show_no_location();  
        console.log(isEmpty(storeLocationDetails));
        
        $(this).attr("disabled", "disabled");
        
        var row = '<tr>' +
            '<td><input type="text" class="form-control" name="name" id="name"></td>' +
            '<td><input type="text" class="form-control" name="department" id="department"></td>' +
        '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>'+
        '</tr>';
        
        // $(this).closest('card').find('i').hide();
          

        var currTable = $(this).closest('table');
        currTable.prepend(row);  
        currTable.find('tbody').find('tr').eq(0).find(".add, .edit").toggle();

        // hide_or_show_no_bus();
        // $("table tbody tr").eq(0).find(".add, .edit").toggle();
        $('[data-toggle="tooltip"]').tooltip();
        if($(this.closest('.collapse')).attr('id')==="collapseExample1"){
          var input = document.getElementById('name');
          // console.log(input);
          var autocomplete = new google.maps.places.Autocomplete(input);
          google.maps.event.addListener(autocomplete, 'place_changed', function () {
              var place = autocomplete.getPlace();
              
              // document.getElementById('city2').value = place.name;
              // Lat = place.geometry.location.lat();
              // Lng = place.geometry.location.lng();
          });
        
          
          }
    });




      // Add row on add button click
      $(document).on("click", ".add", function(){
        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');
        
        input.each(function(){
          if(!$(this).val()){
            $(this).addClass("error");
            empty = true;
          } 
          else{
            $(this).removeClass("error");
          }
        });

        $(this).parents("tr").find(".error").first().focus();

        if(!empty){
          document.getElementById("hide_no_loc_available").style.display = "none";
          var address="hello";
          input.each(function(){
            $(this).parent("td").html($(this).val());
            if(address==="hello"){
              address=$(this).val();
              }
          });     
        
          $(this).parents("tr").find(".add, .edit").toggle();
          $(".add-new").removeAttr("disabled");
        
          if($(this.closest('.collapse')).attr('id')==="collapseExample1"){
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode( { 'address': address}, function(results, status) {
              if (status == google.maps.GeocoderStatus.OK)
              {
                // map.setCenter(results[0].geometry.location);
                //   var contentString = '<div id="content">'+
                // '<div id="siteNotice">'+
                // '</div>'+
                // '<h4 id="firstHeading" class="firstHeading">'+address +'</h4>'+
                // '<div id="bodyContent">'+
                // '<p><i>ARRIVAL:</i></p>'+
                // '<p><i>DEPARTURE:</i></p>'+
                // '<p><i>No. of PSNGR:</i></p>'+
                // '</div>'+
                // '</div>';
                //   sendtocity.push(address);
                // var infowindow = new google.maps.InfoWindow({
                //    content: contentString
                //  });

                var marker = new google.maps.Marker({
                  map: map,
                  title: address,
                  position: results[0].geometry.location,
                  provideRouteAlternatives: true
                });

                // marker.addListener('click', function() {
                //   infowindow.open(map, marker);
                // });

                storeLocationDetails[address]=marker;
                 // boundall();
               
              }
            });
          }
        }   
    });
      

      // Edit row on edit button click
      $(document).on("click", ".edit", function(){    
        $(this).parents("tr").find("td:not(:last-child):not(:first-child)").each(function(){
          $(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
        });   
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
      });


      // Delete row on delete button click
      $(document).on("click", ".delete", function(){
        console.log(storeLocationDetails);
        // hide_or_show_no_location();
        //$(this).closest('card').find('i').hide();
          
        var address=$(this).parents("tr").find("td:first-child").text();
        if($(this.closest('.collapse')).attr('id')==="collapseExample1"){
          storeLocationDetails[address].setMap(null);      
        
          delete storeLocationDetails[address]; 

          hide_or_show_no_location();
          console.log(storeLocationDetails);
        }
        $(this).parents("tr").remove();
        $(".add-new").removeAttr("disabled");
        });
        // hide_or_show_no_bus();
    });



    </script>  

    {% endblock %}
    
