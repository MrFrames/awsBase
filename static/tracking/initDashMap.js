function initMap() {
    if (postQ === "1"){
        myLatLng = {lat: parseFloat(placeLat), lng: parseFloat(placeLng)};
    }
    map = new google.maps.Map(document.getElementById('map'), {
        center: startCoord,
        zoom: 4
    });
    
    console.log("initialising section map:")
    sectionMap = new google.maps.Map(document.getElementById('sectionMap'), {
        center: startCoord,
        zoom: 10
    });
    console.log("initDashMap version:1.0")
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    var markers = [];

    if (postQ === "1"){
        markers.push(new google.maps.Marker({
            map:map,
            title: placeName,
            position: startCoord
        }))
    }
    console.log("1 everything ok...")

    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function(marker) {
        marker.setMap(null);
        });
        markers = [];

        // For each place, get the icon, name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
        return;
        }

        // Create a marker for each place.
        markers.push(new google.maps.Marker({
            map: map,
            title: place.name,
            position: place.geometry.location
        }));
        console.log(" everything ok...")
        markers[markers.length-1]["index"] = markers.length-1

        markers[markers.length-1].addListener('click', function(){
            document.getElementById('lat').value = places[this.index].geometry.location.lat();
            document.getElementById('lng').value = places[this.index].geometry.location.lng();
            document.getElementById('name').value = places[this.index].formatted_address;
        });
        // Auto fills the lat/lng section


        if (place.geometry.viewport) {
            // Only geocodes have viewport.
            bounds.union(place.geometry.viewport);
        } else {
            bounds.extend(place.geometry.location);
        }
    });
    console.log(places[0].geometry.location.lat());
    document.getElementById('lat').value = places[0].geometry.location.lat();
    document.getElementById('lng').value = places[0].geometry.location.lng();
    document.getElementById('name').value = places[0].formatted_address;

    map.fitBounds(bounds);
    });

    google.maps.event.addListener(map,'click',function(event){
        clearMap();
        markers.push(new google.maps.Marker({
            position: {lat: event.latLng.lat(), lng: event.latLng.lng()},
            map: map,
            title: "You clicked here!"
            }));
        document.getElementById('lat').value = event.latLng.lat();
        document.getElementById('lng').value = event.latLng.lng();
    });
    function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }};
    function clearMap(){
        setMapOnAll(null);
        };
    
    /* START OF SECTION MAP FUNCTIONS */
    
    
    
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer({
        draggable: true,
        map: sectionMap
    });
    /*
    directionsDisplay.addListener('directions_changed', function() {
        computeTotalDistance(directionsDisplay.getDirections());
    });
    */
    
    displayRoute('London,Uk', 'Paris,France', directionsService,
        directionsDisplay);
    
    directionsDisplay.addListener('directions_changed', function (e) {
        var result = directionsDisplay.getDirections();
        var wayPoint = result.routes[0].legs[0].via_waypoint; //get waypoint as a result of a user dragging
        var stop = wayPoint.length
        console.log(wayPoint)
        for (i = 0; i<stop; i++){
            console.log(wayPoint[i].location.toString());    
        }  
    });
    /*
    google.maps.event.addListener(directionsDisplay, 'directions_changed', function () {
        document.getElementById('waypoints').innerHTML = "";
        var response = directionsDisplay.getDirections();
        var route = response.routes[0];
        var path = response.routes[0].overview_path;
        var legs = response.routes[0].legs;
        for (i=0;i<legs.length;i++) {
            document.getElementById('waypoints').innerHTML +=  legs[i].start_location.toUrlValue(6) +":";
            document.getElementById('waypoints').innerHTML +=  legs[i].end_location.toUrlValue(6)+"<br>";
        }
    });
    */
    
}

function displayRoute(origin, destination, service, display) {
    service.route({
        origin: origin,
        destination: destination,
        waypoints: [],
        travelMode: 'DRIVING',
        avoidTolls: true
    }, function(response, status) {
        if (status === 'OK') {
            display.setDirections(response);
        } else {
            alert('Could not display directions due to: ' + status);
        } 
    });
}
    

function computeTotalDistance(result) {
    var total = 0;
    var myroute = result.routes[0];
    for (var i = 0; i < myroute.legs.length; i++) {
        total += myroute.legs[i].distance.value;
    }
    total = total / 1000;
    document.getElementById('total').innerHTML = total + ' km';
}