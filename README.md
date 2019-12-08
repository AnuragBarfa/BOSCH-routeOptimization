    <script>
var loc=[];
      function initMap() {
        var myLatLng = {lat: -25.363, lng: 131.044};

        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: myLatLng
        });

        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: 'Hello World!'
        });

             var geocoder = new google.maps.Geocoder();
    document.getElementById('markall').addEventListener('click', function() {
          geocodeAddress(geocoder, map);
        });
      }

 function geocodeAddress(geocoder, resultsMap) {
        for(var i=0;i<loc.length;i++){
        geocoder.geocode({'address': loc[i]}, function(results, status) {
          if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });
            alert("DONE");
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });
      }}



      function onlyUnique(value, index, self) { 
        return self.indexOf(value) === index;
      }
      

      
      function markall(){
        {% for book in books%}
        loc.push("{{book.location}}");
        {% endfor %}
        loc=loc.filter( onlyUnique );
        for(var i=0;i<loc.length;i++)alert(loc[i]);
      }

