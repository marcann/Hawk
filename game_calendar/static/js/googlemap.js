function initializeMap(){
  var venue_pk = event_data[0].fields.venue;
  var venue_lat, venue_lng;
  var name;
  for (var i = 0; i < venues_data.length; i++){
    if (venues_data[i].pk == venue_pk){
      venue_lat = venues_data[i].fields.lat;
      venue_lng = venues_data[i].fields.lng;
      name = venues_data[i].fields.name;
    }
  }

  venue_lat = parseFloat(venue_lat);
  venue_lng = parseFloat(venue_lng);
  
  var location = {
    lat: venue_lat,
    lng: venue_lng
  };

  var var_mapoptions = {
    center: location,
    zoom: 15,
  };

  var var_map = new google.maps.Map(document.getElementById("map_container"), var_mapoptions);

  var var_marker = new google.maps.Marker({
    position: location,
    map: var_map,
    title: name
  });

  var_marker.setMap(var_map);
}
// TODO:30 Add google map to event_detail page.
// TODO:20 Customize Google map view for arena locations.
