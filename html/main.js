$(document).ready(function () {
	//this changes the size of the nav bar and hides the title when you scroll down
	$(window).scroll(function (event) {
            var y = $(this).scrollTop(); //set position from top in pixels
            if (y >= 100) {
                $('.nav').addClass('scroll-nav');
            } else {
                $('.nav').removeClass('scroll-nav');
            }
        });


  // makes the 'back to map' button appear when you scroll down far enough
	
	$(window).scroll(function (event) {
            var y = $(this).scrollTop();
            if (y >= 850) {
                $('.back-to-map').addClass('appear');
            } else {
				 $('.back-to-map').removeClass('appear');

            }
     });


  //for the contact info that pops up when you click 'contact'

  $("li.contact-button").click(function() {
    $(".contact-box").toggleClass("show");
  });

   $(".exit-button").click(function() { //later make this more versatile; anything that needs to appear/disappear when you click it should just be in this
    $(".contact-box").toggleClass("show");
  });
  
});