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

var map;
function initMap() {
    var farhaLocation = {lat: 51.508742, lng: -0.120850}
    var map = new google.maps.Map(document.getElementById('googleMap'), {
        center: farhaLocation,
        zoom: 8
    });
    
    var marker = new google.maps.Marker({position: farhaLocation, map: map});
    
    setMarkers(map);
}

var partOne = [
        ['Calais', -33.890542, 151.274856, 4],
        ['Paris', -33.923036, 151.259052, 5],
        ['Lyon', -34.028249, 151.157507, 3],
        ['Bolognia', -33.80010128657071, 151.28747820854187, 2]
      ];

 function setMarkers(map) {
        // Adds markers to the map.

        // Marker sizes are expressed as a Size of X,Y where the origin of the image
        // (0,0) is located in the top left of the image.

        // Origins, anchor positions and coordinates of the marker increase in the X
        // direction to the right and in the Y direction down.
        var image = {
          url: 'custom-marker.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(20, 32),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(0, 32)
        };
        // Shapes define the clickable region of the icon. The type defines an HTML
        // <area> element 'poly' which traces out a polygon as a series of X,Y points.
        // The final coordinate closes the poly by connecting to the first coordinate.
        var shape = {
          coords: [1, 1, 1, 20, 18, 20, 18, 1],
          type: 'poly'
        };
        for (var i = 0; i < beaches.length; i++) {
          var beach = beaches[i];
          var marker = new google.maps.Marker({
            position: {lat: beach[1], lng: beach[2]},
            map: map,
            icon: image,
            shape: shape,
            title: beach[0],
            zIndex: beach[3]
          });
        }
      }




