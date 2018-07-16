function initSectionMap() {
    sectionMap = new google.maps.Map(document.getElementById('sectionMap'), {
        zoom: 10,
        center: {lat: -24.345, lng: 134.46}  // Australia.
    });

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
    
    displayRoute('Perth, WA', 'Sydney, NSW', directionsService,
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