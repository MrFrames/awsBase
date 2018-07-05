$(document).ready(function () {
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop(); //set position from top in pixels
            if (y >= 100) {
                $('.nav').addClass('scroll-nav');
            } else if (y>=50) {
                $('.title').addClass('disappear');
            } else if (y < 50) {
                $('.nav').removeClass('scroll-nav');
				        $('.title').removeClass('disappear');
                $('.title').removeClass('hidden');
            }
        });



  //makes the fucking title disappear when I want it to

  var windowYPos = window.scrollY;

  $("li").click(function(event) {
    $("h1.title").addClass("hidden");
  });

  // makes the back to map button appear
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop();
            if (y >= 900) {
                $('.back-to-map').addClass('appear');
            } else {
				 $('.back-to-map').removeClass('appear');

            }
     });
  
});