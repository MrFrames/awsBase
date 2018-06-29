$(document).ready(function () {
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop(); //set position from top in pixels
            if (y >= 100) {
                $('.nav').addClass('scroll-nav');
                $('h1.title').addClass('disappear');
            } else {
                $('.nav').removeClass('scroll-nav');
				        $('h1.title').removeClass('disappear');
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

// $('a').click(function (event) {
//       event.preventDefault();
//       $('html, body').stop(){
//         scrollTop: $( $(this).attr('href') ).offset(100).top
//       };
//     });
  
});


function initMap() {
    var sectionNames = Object.keys(secPlaces);
    var forLimit = sectionNames.length;
    var polygons = [];
    map = new google.maps.Map(document.getElementById('googleMap'),{
        center: {lat: 51.5287718, lng: -0.2416808},
        zoom: 9,
        styles: [
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
          ]

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

