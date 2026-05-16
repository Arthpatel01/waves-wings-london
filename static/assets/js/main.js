jQuery(document).on(
  "ready",
  (function ($) {
    "use strict";

    /*--------------------------
        SCROLLSPY ACTIVE
    ---------------------------*/
    $("body").scrollspy({
      target: ".bs-example-js-navbar-scrollspy",
      offset: 50,
    });

    /*--------------------------
        STICKY MAINMENU
    ---------------------------*/
    $("#mainmenu-area").sticky({
      topSpacing: 0,
    });

    /*-----------------------------
        SLIDER ACTIVE
    ------------------------------*/
    var mySlider = $(".pogoSlider")
      .pogoSlider({
        pauseOnHover: false,
      })
      .data("plugin_pogoSlider");

    /*----------------------------
        OPEN SEARCH FORM
    ----------------------------*/
    var $searchForm = $(".search-form");
    var $searchFormTrigger = $(".search-form-trigger");
    var $formOverlay = $(".search-form-overlay");
    $searchFormTrigger.on("click", function (event) {
      event.preventDefault();
      toggleSearch();
    });

    function toggleSearch(type) {
      if (type === "close") {
        //close serach
        $searchForm.removeClass("is-visible");
        $searchFormTrigger.removeClass("search-is-visible");
      } else {
        //toggle search visibility
        $searchForm.toggleClass("is-visible");
        $searchFormTrigger.toggleClass("search-is-visible");
        if ($searchForm.hasClass("is-visible"))
          $searchForm.find('input[type="search"]').focus();
        $searchForm.hasClass("is-visible")
          ? $formOverlay.addClass("is-visible")
          : $formOverlay.removeClass("is-visible");
      }
    }

    /*------------------------------
        TIME PICKER ACTIVE
    -------------------------------*/
    var input = $("#time").clockpicker({
      placement: "bottom",
      align: "left",
      autoclose: true,
      default: "now",
    });

    /*--------------------------
       HOME PARALLAX BACKGROUND
    ----------------------------*/
    $(window).stellar({
      responsive: true,
      positionProperty: "position",
      horizontalScrolling: false,
    });

    /*------------------------------
        VIDEO BLOG POPUP
    --------------------------------*/
    $(".blog-video-button").magnificPopup({
      disableOn: 700,
      type: "iframe",
      mainClass: "mfp-fade",
      removalDelay: 320,
      preloader: false,
    });

    /*---------------------------
        SMOOTH SCROLL
    -----------------------------*/
    $("a.scrolltotop, .slider-area h3 a, .navbar-header a, ul#nav a").on(
      "click",
      function (event) {
        var id = $(this).attr("href");
        var offset = 40;
        var target = $(id).offset().top - offset;
        $("html, body").animate(
          {
            scrollTop: target,
          },
          1500,
          "easeInOutExpo"
        );
        event.preventDefault();
      }
    );

    /*----------------------------
        SCROLL TO TOP
    ------------------------------*/
    $(window).on("scroll", function () {
      var $totalHeight = $(window).scrollTop();
      var $scrollToTop = $(".scrolltotop");
      if ($totalHeight > 300) {
        $scrollToTop.fadeIn();
      } else {
        $scrollToTop.fadeOut();
      }
      if ($totalHeight + $(window).height() === $(document).height()) {
        $scrollToTop.css("bottom", "90px");
      } else {
        $scrollToTop.css("bottom", "20px");
      }
    });

    /*---------------------------
        MENU LIST MIXITUP FILTERING
    ----------------------------*/
    $(".food-menu-list").mixItUp();

    /*---------------------------
        MENU DISCOUNT SLIDER
    -----------------------------*/
    /*$(".menu-discount-offer").owlCarousel({
      merge: true,
      video: true,
      items: 1,
      smartSpeed: 1000,
      loop: true,
      nav: false,
      navText: [
        '<i class="fa fa-angle-left"></i>',
        '<i class="fa fa-angle-right"></i>',
      ],
      autoplay: false,
      autoplayTimeout: 2000,
      margin: 15,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 1,
        },
        1000: {
          items: 1,
        },
      },
    });*/

    /*---------------------------
        MENU DISCOUNT SLIDER
    -----------------------------*/
    // 1. Count how many promotions actually exist on the page
    var $discountSlider = $(".menu-discount-offer");
    var discountItemCount = $discountSlider.children(".single-promotions").length;

    $discountSlider.owlCarousel({
      merge: true,
      video: true,
      items: 1,
      smartSpeed: 1000,

      // 2. THE FIX: Only enable infinite loop if there is more than 1 item!
      loop: discountItemCount > 1,

      nav: false,
      navText: [
        '<i class="fa fa-angle-left"></i>',
        '<i class="fa fa-angle-right"></i>',
      ],
      autoplay: false,
      autoplayTimeout: 2000,
      margin: 15,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 1,
        },
        1000: {
          items: 1,
        },
      },
    });

    /*---------------------------
        TEAM SLIDER
    -----------------------------*/
    /*$(".team-slider").owlCarousel({
      merge: true,
      video: true,
      items: 1,
      smartSpeed: 1000,
      loop: true,
      nav: false,
      navText: [
        '<i class="fa fa-angle-left"></i>',
        '<i class="fa fa-angle-right"></i>',
      ],
      autoplay: false,
      autoplayTimeout: 2000,
      margin: 15,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 3,
        },
        1000: {
          items: 4,
        },
        1200: {
          items: 5,
        },
      },
    });*/

    /*---------------------------
        TEAM SLIDER (Perfect Sizing & Centering Fix)
    -----------------------------*/
    var $teamSlider = $(".team-slider");
    var chefCount = $teamSlider.children(".single-team-member").length;

    // Apply the centering class only if the tray isn't completely full
    if (chefCount < 5) {
        $teamSlider.addClass("justify-center-owl");
    }

    $teamSlider.owlCarousel({
      merge: true,
      video: true,
      smartSpeed: 1000,
      margin: 15,
      responsiveClass: true,

      // Control carousel functions safely based on your total item counts
      loop: chefCount > 5,
      autoplay: chefCount > 5,
      autoplayTimeout: 2000,
      dots: chefCount > 5,
      nav: false,

      responsive: {
        0: {
          items: 1,
          loop: chefCount > 1
        },
        600: {
          items: 3,
          loop: chefCount > 3
        },
        1000: {
          items: 4,
          loop: chefCount > 4
        },
        1200: {
          // FORCES the exact "1 of 5" default sizing rule on large desktop screens!
          items: 5
        },
      },
    });

    /*---------------------------
        BLOG POST SLIDER
    -----------------------------*/
    $(".post-slider").owlCarousel({
      merge: true,
      video: true,
      items: 1,
      smartSpeed: 2000,
      loop: true,
      nav: true,
      navText: [
        '<i class="fa fa-angle-left"></i>',
        '<i class="fa fa-angle-right"></i>',
      ],
      autoplay: true,
      autoplayTimeout: 3000,
      margin: 15,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 1,
        },
        1000: {
          items: 2,
        },
        1200: {
          items: 3,
        },
      },
    });

    /*---------------------------
        BLOG POST IMAGE SLIDER
    -----------------------------*/
    $(".blog-image-sldie").owlCarousel({
      merge: true,
      video: true,
      items: 1,
      smartSpeed: 1000,
      loop: true,
      animateIn: "fadeIn",
      animateOut: "fadeOut",
      nav: true,
      navText: [
        '<i class="fa fa-angle-left"></i>',
        '<i class="fa fa-angle-right"></i>',
      ],
      autoplay: false,
      autoplayTimeout: 2000,
      margin: 15,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 1,
        },
        1000: {
          items: 1,
        },
      },
    });

    /*---------------------------
        BMENU SLIDER
    -----------------------------*/
    $(".food-menu-list.food-menu-slider").owlCarousel({
      smartSpeed: 1000,
      loop: true,
      nav: true,
      navText: [
        '<i class="fa fa-angle-left"></i>',
        '<i class="fa fa-angle-right"></i>',
      ],
      autoplay: true,
      autoplayTimeout: 3000,
      margin: 30,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 2,
        },
        1000: {
          items: 3,
        },
      },
    });

    /*---------------------------
        RESTAURANT GALLERY SLIDER
    -----------------------------*//*
    var $gallerySlider = $(".restaurant-gallery-slider");
    var galleryItemCount = $gallerySlider.children(".single-gallery-item").length;

    $gallerySlider.owlCarousel({
        margin: 20,
        // Only loop if there are enough items to avoid the Owl Carousel crash bug!
        loop: galleryItemCount > 3,
        nav: false,
        dots: true,              // Shows little navigation dots at the bottom
        autoplay: true,          // Auto-scrolls to keep the page feeling alive
        autoplayTimeout: 3000,
        smartSpeed: 800,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1         // 1 photo on mobile phones
            },
            600: {
                items: 2         // 2 photos on tablets
            },
            1000: {
                items: 3         // 3 photos on standard desktop
            },
            1200: {
                items: 4         // 4 photos on large HD monitors
            }
        }
    });*/

    /*---------------------------
        RESTAURANT GALLERY SLIDER
    -----------------------------*/
    var $gallerySlider = $(".restaurant-gallery-slider");
    var galleryItemCount = $gallerySlider.children(".single-gallery-item").length;

    $gallerySlider.owlCarousel({
        margin: 20,
        loop: galleryItemCount > 3,

        // RESTORE THE RED NAVIGATION ARROWS
        nav: true,
        navText: [
            '<i class="fa fa-angle-left"></i>',
            '<i class="fa fa-angle-right"></i>',
        ],
        dots: false, // Hide the dots to match the old style

        autoplay: true,
        autoplayTimeout: 3000,
        smartSpeed: 800,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    });

    /*----------------------------
        INSTAGRAM FEED ACTIVE
    -----------------------------*/
	/*var instaCount = 97;
	    var feed = new Instafeed({
      accessToken: 'IGQVJXQ0laY2E4MTVNMjZAjX1diSWRHT0tJckFUNG9RZA2hnUmRwQ2V5cHo1M0ZAwV1pLeGYxdE93UWJSYTdOVHR1ZAWU4SnduaHp0U09mTGUxd3dIRGVfSEl0bDd6S0s1Q2FqUkhaVlozdTUzS1RsaGROSgZDZD',
	   target: "instagram",
	   limit:4,
	       template: '<div class="box {{count}}"><a href="{{link}}"><img class="img-responsive" src="{{image}}" /></a></div>',
    resolution: 'low_resolution',
	 transform: function(item) {
      item.count =String.fromCharCode(instaCount++)
       return item;
    }
    });
    feed.run();*/

    /*--------------------------
        ACTIVE WOW JS
    ----------------------------*/
    new WOW().init();
  })(jQuery)
);

jQuery(window).on("load", function () {
  /*--------------------------
        PRE LOADER
    ----------------------------*/
  $(".preeloader").fadeOut(1000);
});
