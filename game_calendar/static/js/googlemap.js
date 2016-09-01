function initMap() {
  var mapDiv = document.getElementById('map');
  var map = new google.maps.Map(mapDiv, {
    center: {lat: 44.540, lng: -78.546},
    zoom: 8
  });
}

// DOING:20 Add google map to event_detail page.
// DOING:40 Customize Google map view for arena locations.
