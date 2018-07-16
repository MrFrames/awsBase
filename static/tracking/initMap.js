function initMap() {

    map = new google.maps.Map(document.getElementById('googleMap'),{
        center: {lat: 51.5287718, lng: -0.2416808},
        zoom: 9,
        styles: getStyle()
    });

    console.log("version2.4")
    
    var latlng = []
    bounds = new google.maps.LatLngBounds();
    polygons = [];
    
    console.log(allPosts[0])

    var posts = setMarkers(map,allPosts,getPostPin());
    var meets = setMarkers(map,allMeetUps,getMeetUpPin());
    
    addInfoWindows(map,posts,"post");
    addInfoWindows(map,meets,"meetUps");
    
    var requestArray = [];
    directionServices = [];
    directionDisplays = [];
    setRoutes(map, requestArray, directionServices, "route", planPlaces);
    
    histRequestArray =[];
    histDirectionsServices =[];
    histDirectionDisplays = [];
    setRoutes(map, histRequestArray, histDirectionsServices, "hist", hist_sections);
    
    
    setPolys(map);
    
    console.log(polySecNames);
    
    setBounds(planPlaceNames, map);

    map.fitBounds(bounds);

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

function getStyle(){
    return[
            {elementType: 'geometry', 
             stylers: [{color: '#fafae3'}]},
            {elementType: 'labels.text.stroke', 
             stylers: [{color: '#000000'},
                      {strokeWeight: '1'},
                      {visibility: 'off'}]},
            
            {elementType: 'labels.text.fill', 
             stylers: [{color: '#58310d'},
                      {fontWeight: '400'}]},
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text.fill',
              stylers: [{/*fontFamily: 'Fira Sans'*/},
                        {color: '#58310d'}]
            },
            
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text',
              stylers: [{fontFamily: 'Fira Sans'},
                        {color: '#58310d'},
                       {fontWeight: '900'}]
            },
            
            {
              featureType: 'poi',
              elementType: 'labels.text.fill',
              stylers: [{color: '#58310d'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{color: '#efedd0'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9a6b83'}]
            },

            {
              featureType: 'road',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9ca5b3'}]
            },
            {
              featureType: 'road.local',
              elementType: 'geometry',
              stylers: [{color: '#e3e0bd'},
                       {weight: 1}]
            },
            {
              featureType: 'road.arterial',
              elementType: 'geometry',
              stylers: [{color: '#e3e0bd'},
                        {weight: 1}
                       /*{visibility: 'off'}*/]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry',
              stylers: [{color: '#c3bc89'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry.stroke',
              stylers: [{color: '#c3bc89'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'labels.text.fill',
              stylers: [{color: '#f3d19c'}]
            },
            {
              featureType: 'transit',
              elementType: 'geometry',
              stylers: [{color: '#2f3948'},
                       {visibility: 'off'}]
            },
            {
              featureType: 'transit.station',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{color: '#cac392'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.fill',
              stylers: [{color: '#cac392'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.stroke',
              stylers: [{color: '#cac392'}]
            }
          ];
}

function getPostContent(postObj){
    return ('<div class = "postBox">' +
            '<h1>' + postObj[2] + '</h1><br/>' +
            '<p>' + postObj[3] + '</p>' +
            '<img src =' + postObj[5] + ' width=100%><br/>' +
            '<p>' + postObj[4] + '<br/>' +
            '<a href="http://127.0.0.1:8000/blog/?pk=' + postObj[6] + '">read more...</a></p></div>' +
			'</div>')
}

function getMeetupContent(meetUpObj){
    return('<h1>' + String(meetUpObj[2]) + '</h1>' +
           '<h2><a href="mailto:farha.beee@gmail.com">Email me to meet up!<br/>' +
           'farha.beee@gmail.com</a></h2>')
}

function getMeetUpPin(){
    return {
        url: meetIconPath,
        //size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(16, 32)
    };
}

function getPostPin(){
    return {
        url: postIconPath,
        //size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(16, 32)
    };
}

function setPoly(secName,color,poly){
    var new_poly = (new google.maps.Polyline({
            name: secName,
            path: poly,
            geodesic: false,
            strokeColor: color,
            strokeOpacity: 0.8,
            strokeWeight: 3
            })
        );
    return new_poly
}

function setPolys(map){
    console.log("polys...")
    /*
    Below loops through the sections, then each place in the
    section, adding it's lat/lon coords to the polygons array.
    */
    for (i = 0; i < polySecNames.length; i++){
        var start = [polySecPlaces[polySecNames[i]]["start"]];
        var end = polySecPlaces[polySecNames[i]]["end"];
        var places = polySecPlaces[polySecNames[i]]["places"];

        

        var poly = start.concat(places);
        poly.push(end);

        console.log(poly);

        for (x=0; x < poly.length; x++){
            bounds.extend(poly[x]);
            }

        /*
        Below pushes a google.maps.Polyline object to
        the polygons array for each section, using the poly array as
        the path. Then the .setMap method is used to apply the last
        (current) Polyline object in the Polygons array to the map.
        */
        polygons.push(setPoly(polySecNames[i],polySecPlaces[polySecNames[i]]["color"],poly))

        polygons[polygons.length-1].setMap(map);

        google.maps.event.addListener(polygons[i],'click',function() {setToSection(this.name,map,posts,meets,polygons,image)})
    }
}

function setBounds(sectionNames){
    for (i = 0; i < sectionNames.length; i++){
        var poly = secPlaces[sectionNames[i]]["places"];
        for (x=0; x < poly.length; x++){
            bounds.extend(poly[x]);
        }
    }
}

function setMarkers(map,markers,icon) {
  var markerArray = [];

  var shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: 'poly'
  };

  for (var i = 0; i < markers.length; i++) {
    var post = markers[i];
    markerArray.push(new google.maps.Marker({
      position: {lat: post[0], lng: post[1]},
      map: map,
      icon: icon,
      shape: shape,
      title: post[2]
    }));
      //markerArray[markerArray.length-1].setMap(map);
  }
  return markerArray
}

function addInfoWindows(map,objs,type){
    
    
    for (x = 0;x < objs.length;x++){
        var contentString = "";
        if (type === "post"){
            contentString = getPostContent(allPosts[x]);
        } else {
            contentString = getMeetupContent(allMeetUps[x]);
        };
        
        objs[x].info = new google.maps.InfoWindow({
            content: contentString,
            maxWidth: 300
        });
        objs[x].addListener('click', function(){
            this.info.open(this.get('map'),this);
        });
    };
    
}

function setRoutes(map, requestArray,directionServices, routeType, secPlaces) {
    if (routeType === "route"){
        console.log("Route places:")
    } else {
        console.log("Hist places:")
    }
    console.log(secPlaces)
    var sectionNames = Object.keys(secPlaces);
    console.log(sectionNames.length)
    for (cur = 0; cur < sectionNames.length; cur++){
        console.log(sectionNames[cur]);
        var wayCoords = secPlaces[sectionNames[cur]]["places"];

        var start = secPlaces[sectionNames[cur]]["start"];
        var end = secPlaces[sectionNames[cur]]["end"];

        var waypoints = []
        for (coord in wayCoords){
            latlng = wayCoords[coord];
            waypoints.push({location:{lat:latlng.lat,lng:latlng.lng}});
        }
        request = getDirectionRequest(start,end,waypoints, "WALKING");
        requestArray.push(request);
        
        //colorArray.push(secPlaces[sectionNames[cur]]["color"]);
        
        directionServices.push(new google.maps.DirectionsService);

    }
    console.log("routeType to processRequest:")
    console.log(routeType)
    processRequest(requestArray,directionServices, routeType);
}

function processRequest(requestArray,directionServices, routeType){
    var n = 0;
    function submitRequest(requestArray,directionServices,routeType){
        console.log("route type to submit request:")
        console.log(routeType);
        console.log(requestArray);
        if (routeType === "route"){
            directionServices[n].route(requestArray[n],directionResults1);
        } else {
            console.log("hist req:")
            directionServices[n].route(requestArray[n],directionResults2);
        }
        function directionResults1(result,status){
            // callback function sets route on maps
            if (status === google.maps.DirectionsStatus.OK){
                console.log("applying callback... ")
                
                console.log(status);
                if (status === google.maps.DirectionsStatus.OK){
                    directionDisplays.push(new google.maps.DirectionsRenderer({suppressMarkers: true, polylineOptions: {strokeColor:"brown"}}));
                    directionDisplays[directionDisplays.length-1].setDirections(result);
                    directionDisplays[directionDisplays.length-1].setMap(map);
                    //console.log("directionLength" + directionDisplays.length);
                }
            } else {
                setTimeout(function(){
                    directionsServices[directionDisplays.length-1].route(requestArray[directionDisplays.length-1],directionResults1);
                    
                }, 250);
            }
        }
        function directionResults2(result,status){
            console.log(histDirectionDisplays.length)
            if (status === google.maps.DirectionsStatus.OK){
                console.log(status);
                // callback function sets route on maps
                if (status === google.maps.DirectionsStatus.OK){
                    histDirectionDisplays.push(new google.maps.DirectionsRenderer({suppressMarkers: true, polylineOptions: {strokeColor:"black"}}));
                    histDirectionDisplays[histDirectionDisplays.length-1].setDirections(result);
                    histDirectionDisplays[histDirectionDisplays.length-1].setMap(map);
                    if (histDirectionDisplays.length === directionServices.length){
                        map.fitBounds(bounds);
                        console.log("Fitting Bounds!!!")
                    }
                }
            } else {
                setTimeout(function(){
                    histDirectionsServices[histDirectionDisplays.length-1].route(histRequestArray[histDirectionDisplays.length-1],directionResults2);
                }, 250);
            }
        }
        if (n<requestArray.length-1){
            console.log(n);
            n++
            submitRequest(requestArray,directionServices,routeType);
        }
    }
    submitRequest(requestArray,directionServices,routeType);
}




function setToSection(sectionName,map,posts,meets,polygons,icon){
    var new_bounds = new google.maps.LatLngBounds();
    //wipeMap(map,posts,meets,polygons);
    waypoints = secPlaces[sectionName]["places"];
    console.log(waypoints);
    for (var index in waypoints){
        console.log(waypoints[index]);
        new_bounds.extend(waypoints[index]);
    }
    map.fitBounds(new_bounds);
    new_bounds = null;
    //posts = secPlaces[sectionName]["posts"];
    //meetUps = secPlaces[sectionName]["meetUps"];
    //setPoly(sectionName,secPlaces[sectionName]["color"],waypoints).setMap(map)
    //setMarkers(map,posts,icon);
    //setMarkers(map,meetUps,icon);

}

function wipeMap(map,posts,meets,polygons){
    setMapOnAll(null,posts);
    setMapOnAll(null,meets);
    setMapOnAll(null,polygons);
}

function setMapOnAll(map,markers) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}