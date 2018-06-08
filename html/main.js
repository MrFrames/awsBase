$(document).ready(function () {
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop(); //set position from top in pixels
            if (y >= 100) {
                $('.nav').addClass('scroll-nav');
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


function mainMap() {
var mapProp= {
    center:new google.maps.LatLng(51.508742,-0.120850),
    zoom:10,
};
var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
} 