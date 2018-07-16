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
    console.log("initDashMap version:1.1")
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
    
    // Search box function:

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

            console.log("everything ok...")
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
        document.getElementById('name').value = "Clicked";
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
    
    var directionService = new google.maps.DirectionsService;
    var directionsDisplay;
    
    var start = ""
    var end = ""
    
    google.maps.event.addListener(sectionMap,'click',function(event){
        if (!start){
            startMarker = new google.maps.Marker({
                position: {lat: event.latLng.lat(), lng: event.latLng.lng()},
                map: sectionMap,
                title: "Start"
            });
            start = {lat: event.latLng.lat(), lng: event.latLng.lng()};
            document.getElementById('start').value = JSON.stringify(start);
        } else if (!end){
            startMarker.setMap(null);
            end ={lat: event.latLng.lat(), lng: event.latLng.lng()};
            document.getElementById('end').value = JSON.stringify(end);
            console.log("start/end:")
            console.log(start)
            console.log(end)
        
            var request = getDirectionRequest(start,end,[],"BICYCLING");
            directionService.route(request,directionResults);
        
            function directionResults (result, status){
                directionsDisplay = new google.maps.DirectionsRenderer({
                    draggable: true,
                    map: sectionMap
                });
                directionsDisplay.setDirections(result);
                directionsDisplay.setMap(sectionMap);
                directionsDisplay.addListener('directions_changed', function () {
                    var result = directionsDisplay.getDirections();
                    var wayPoint = result.routes[0].legs[0].via_waypoint; //get waypoint as a result of a user dragging
                    
                    start = result.routes[0].legs[0].start_location;
                    startCoord = {"lat": start.lat(), "lng": start.lng()};
                    startString = JSON.stringify(startCoord);
                    document.getElementById("start").value = startString;
                    
                    end = result.routes[0].legs[0].end_location;
                    endCoord = {"lat": end.lat(), "lng": end.lng()};
                    endString = JSON.stringify(endCoord);
                    document.getElementById("end").value = endString;

                    var waypoints = {};
                    var waypointString = "";

                    console.log(wayPoint)
                    for (i = 0; i<wayPoint.length; i++){
                        console.log(wayPoint[i].location.lat());
                        lat = wayPoint[i].location.lat();
                        lng = wayPoint[i].location.lng();
                        wayCoord = {"lat": lat, "lng": lng};
                        waypoints[i] = wayCoord;
                    };
                waypointString = JSON.stringify(waypoints);
                console.log(waypointString);
                document.getElementById("waypoints").value = waypointString;
                });
            };
        };
        
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

function getDirectionRequest(start,end, waypoints, travelMode){
    return {
        origin: start,
        destination: end,
        travelMode: travelMode,
        waypoints: waypoints,
        optimizeWaypoints: true,
    };
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

function initDropdown(){
    var post_names = Object.keys(posts);
    console.log(post_names)
    var option_list = [];
    for (i=0; i<post_names.length; i++){
        name = post_names[i];
        console.log(name);
        option_list.push(document.createElement("option"));
        option_list[option_list.length-1].value = name;
        option_list[option_list.length-1].innerHTML = name;
        document.getElementById("post names").appendChild(option_list[option_list.length-1]);
    }
}

function auto_fill(){
    name = document.getElementById("post names").value;
    console.log("name from dropdown:");
    console.log(name);
    coord = posts[name]["coord"];
    
    document.getElementById('placePk').value = posts[name]["placePk"];
    document.getElementById('name').value = posts[name]["place_name"];
    document.getElementById('lat').value = coord["lat"];
    document.getElementById('lng').value = coord["lng"];

    document.getElementById('postPk').value = posts[name]["postPk"];
    document.getElementById('post_title').value = name;
    quill.root.innerHTML = posts[name]["content"];
}