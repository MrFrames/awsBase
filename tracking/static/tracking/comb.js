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
    var polygons = [];
    map = new google.maps.Map(document.getElementById('googleMap'),{
        center: {lat: 51.5287718, lng: -0.2416808},
        zoom: 9
    });

    /*
    Below loops through the sections, then each place in the
    section, adding it's lat/lon coords to the polys array.
    */

    for (i = 0; i < forLimit; i++){
        places = secPlaces[sectionNames[i]]["places"];
        poly = [];
        for (x=0; x < places.length; x++){
            poly.push({lat:places[x][1],lng:places[x][2]});
            }

        /*
        Below pushes a google.maps.Polyline object to
        the polygons array for each section, using the poly array as
        the path. Then the .setMap method is used to apply the last
        (current) Polyline object in the Polygons array to the map.
        */

        polygons.push(new google.maps.Polyline({
            path: poly,
            geodesic: false,
            strokeColor: secPlaces[sectionNames[i]]["color"],
            strokeOpacity: 0.45,
            strokeWeight: 3
            })
        );
    polygons[polygons.length -1].setMap(map);
    }
}