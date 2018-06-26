$(document).ready(function () {
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop(); //set position from top in pixels
            if (y >= 100) {
                $('.nav').addClass('scroll-nav');
            } else if (y>=50) {
                $('.title').addClass('disappear');
            } else {
                $('.nav').removeClass('scroll-nav');
				$('.title').removeClass('disappear');
            }
        });
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop();
            if (y >= 900) {
                $('.back-to-map').addClass('appear');
            } else {
				 $('.back-to-map').removeClass('appear');

            }
     });
  
});

function initMap() {

    var forLimit = sectionNames.length;
    var polygons = [];
    map = new google.maps.Map(document.getElementById('googleMap'),{
        center: {lat: 51.5287718, lng: -0.2416808},
        zoom: 9
    });
    var latlng = []
    var bounds = new google.maps.LatLngBounds();
    
    var image = {
        url: iconPath,
        //size: new google.maps.Size(32, 32),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(16, 32)
    };

    var posts = setMarkers(map,allPosts,image);
    var meets = setMarkers(map,allMeetUps,image);

    /*
    Below loops through the sections, then each place in the
    section, adding it's lat/lon coords to the polys array.
    */

    for (i = 0; i < forLimit; i++){
        poly = secPlaces[sectionNames[i]]["places"];
        for (x=0; x < poly.length; x++){
            bounds.extend(poly[x]);
            }

        /*
        Below pushes a google.maps.Polyline object to
        the polygons array for each section, using the poly array as
        the path. Then the .setMap method is used to apply the last
        (current) Polyline object in the Polygons array to the map.
        */

        polygons.push(setPoly(sectionNames[i],secPlaces[sectionNames[i]]["color"],poly))

        polygons[i].setMap(map);
    
        google.maps.event.addListener(polygons[i],'click',function() {setToSection(this.name,map,posts,meets,polygons,image)})
    }

    map.fitBounds(bounds);

}

function setPoly(secName,color,poly){
    var new_poly = (new google.maps.Polyline({
            name: secName,
            path: poly,
            geodesic: false,
            strokeColor: color,
            strokeOpacity: 0.45,
            strokeWeight: 10
            })
        );
    return new_poly
}

function get_postWindowContent(post){
  title = post[2]
  image = post[3]
  content = post[4]

  var content_string = "<h1>" + title + "</h1><br/>" +
  "<img src = '" + image + "'><br/>" +
  "<p>" + content + "</p>"

  return content_string
}

function setMarkers(map,markers,icon) {
  var mArray = [];
  var iArray = [];

  var shape = {
    coords: [1, 1, 1, 20, 18, 20, 18, 1],
    type: 'poly'
  };

  for (var i = 0; i < markers.length; i++) {
    var post = markers[i];
    content_string = "IT WORKED!!!"
    iArray.push(new google.maps.InfoWindow({
      content:content_string,
      maxWidth = 200
    }));
    console.log(content_string)
    mArray.push(new google.maps.Marker({
      position: {lat: post[0], lng: post[1]},
      map: map,
      icon: icon,
      shape: shape,
      title: post[2]
    }));
  }
  for (var i = 0; i < markers.length; i++) {
    mArray[i].addListener('click',function(){
      iArray[i].open(map,mArray[i]);
    })
  }
}

  return iArray
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
    posts = secPlaces[sectionName]["posts"];
    meetUps = secPlaces[sectionName]["meetUps"];
    //setPoly(sectionName,secPlaces[sectionName]["color"],waypoints).setMap(map)
    setMarkers(map,posts,icon);
    setMarkers(map,meetUps,icon);
    
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