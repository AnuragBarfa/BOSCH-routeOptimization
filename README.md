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
		<div id="map" style="position:relative;width:100%;height: 600px;float:left;"></div>
		<div id="over_map" class="pull-right">
			<!-- <button>Location</button>
			<button>Location</button> -->
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
                <table class="table">
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>P. No.</th>
                        <th><button type="button" class="btn btn-info add-new"><!-- <i class="fa fa-plus"></i> -->Add Loc</button></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>John Doe</td>
                        <td>20</td>
                        <td>
              <a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a>
                            <a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a>
                            <a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>Peter Parker</td>
                        <td>15</td>
                        <td>
              <a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a>
                            <a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a>
                            <a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>
                        </td>
                    </tr>
                    <tr>
                        <td>Fran Wilson</td>
                        <td>16</td>
                        <td>
              <a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a>
                            <a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a>
                            <a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a>
                        </td>
                    </tr>      
                </tbody>
            </table>
              </div>
            </div>
            
        </div>

			
			<br>
			<p>
			  <a class="btn btn-primary" data-toggle="collapse" href="#collapseExample2" role="button" aria-expanded="false" aria-controls="collapseExample2">
			    Bus
			  </a>
			</p>
			<div class="collapse" id="collapseExample2">
			  <div class="card card-body">
			    <input type="" name="">
			  </div>
			</div>
		</div>
	</div>
{% endblock %}

{% block javascript %}
</script>
  <script>
      var map;
      var storeLocationDetails={};
      function initMap() {
        var myLatLng = {lat: 20.593684, lng: 78.96288000000004};

        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: myLatLng,
          disableDefaultUI: true
        });

        // var marker = new google.maps.Marker({
        //   position: myLatLng,
        //   map: map,
        //   title: 'Hello World!'
        // });

        // var input2 = document.getElementById('form-id');
        // var autocomplete2 = new google.maps.places.Autocomplete(input2);
        // google.maps.event.addListener(autocomplete2, 'place_changed', function () {
        //     var place = autocomplete2.getPlace();
        // });
      }
      function addMarker(location) {
        console.log("in marker");
        marker = new google.maps.Marker({
            position: location,
            map: map
        });
      }
  </script>
  <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDmwBs8dSuwg56fTWsbJyMdrvXYU3_Pim4&libraries=places&callback=initMap">
  </script>
  <script type="text/javascript">
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
  var actions = $("table td:last-child").html();
  // Append table with add row form on add new button click
    $(".add-new").click(function(){
      $(this).attr("disabled", "disabled");
      var index = $("table tbody tr:last-child").index();
          var row = '<tr>' +
              '<td><input type="text" class="form-control" name="name" id="name"></td>' +
              '<td><input type="text" class="form-control" name="department" id="department"></td>' +
        '<td>' + actions + '</td>' +
          '</tr>';
        $("table").prepend(row);   
      $("table tbody tr").eq(0).find(".add, .edit").toggle();
      $('[data-toggle="tooltip"]').tooltip();
      var input = document.getElementById('name');
      console.log(input);
      var autocomplete = new google.maps.places.Autocomplete(input);
      // var Lat;
      // var Lng;
      // var Loc;
      google.maps.event.addListener(autocomplete, 'place_changed', function () {
          var place = autocomplete.getPlace();
          // document.getElementById('city2').value = place.name;
          // Lat = place.geometry.location.lat();
          // Lng = place.geometry.location.lng();
      });
    });
  // Add row on add button click
  $(document).on("click", ".add", function(){
    var empty = false;
    var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
      if(!$(this).val()){
        $(this).addClass("error");
        empty = true;
      } else{
                $(this).removeClass("error");
            }
    });
    $(this).parents("tr").find(".error").first().focus();
    if(!empty){
      var address="hello";
      input.each(function(){
        $(this).parent("td").html($(this).val());
        if(address==="hello"){
          address=$(this).val();
        }
      });     
      $(this).parents("tr").find(".add, .edit").toggle();
      $(".add-new").removeAttr("disabled");
      var CurrLocation;
      var Lat2="hello";
      var Lng2;
      var geocoder = new google.maps.Geocoder();
      geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK)
        {
            // map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: map,
              position: results[0].geometry.location
            });
            storeLocationDetails[address]=marker;
        }
      });
      console.log(Lat2);
      console.log(Lng2);
      CurrLocation = new google.maps.LatLng(Lat2,Lng2);
      console.log("bef marker");
      addMarker(CurrLocation);
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
    $(this).parents("tr").remove();
    $(this).parents("tr").remove();
    $(".add-new").removeAttr("disabled");
    });
});
</script>  
<script src="{% static 'js/jquery-3.1.1.min.js' %}"></script>  
<script src="{% static 'js/bootstrap.min.js' %}"></script>
<script src="{% static 'js/plugin.js' %}"></script>
{% endblock %}
<!-- 
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bootstrap Table with Add and Delete Row Feature</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto|Varela+Round|Open+Sans">
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>


</head>
<body>
    <div class="container">
        
    </div>     
</body>
</html>                             -->
