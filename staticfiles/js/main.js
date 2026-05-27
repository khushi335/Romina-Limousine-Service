(function ($) {
    "use strict";

    /* =========================
       1. Spinner
    ========================= */
    const spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 100);
    };
    spinner();

    /* =========================
       2. WOW.js Init
    ========================= */
    if (typeof WOW !== "undefined") {
        new WOW().init();
    }

    /* =========================
       3. Sticky Navbar
    ========================= */
    $(window).on("scroll", function () {
        if ($(this).scrollTop() > 200) {
            $('.sticky-top').addClass('shadow-sm').css('top', '0px');
        } else {
            $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
        }
    });

    /* =========================
       4. Car Categories Carousel
    ========================= */
    if ($(".categories-carousel").length) {
        $(".categories-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            dots: false,
            loop: true,
            margin: 25,
            nav: true,
            navText: [
                '<i class="fas fa-chevron-left"></i>',
                '<i class="fas fa-chevron-right"></i>'
            ],
            responsiveClass: true,
            responsive: {
                0: { items: 1 },
                576: { items: 1 },
                768: { items: 1 },
                992: { items: 2 },
                1200: { items: 3 }
            }
        });
    }

    /* =========================
       5. Testimonial Carousel
    ========================= */
    if ($(".testimonial-carousel").length) {
        $(".testimonial-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1500,
            center: false,
            dots: true,
            loop: true,
            margin: 25,
            nav: false,
            responsiveClass: true,
            responsive: {
                0: { items: 1 },
                576: { items: 1 },
                768: { items: 1 },
                992: { items: 2 },
                1200: { items: 2 }
            }
        });
    }

    /* =========================
       6. Vehicle Selection Logic
    ========================= */
    document.addEventListener("DOMContentLoaded", function () {

        const cards = document.querySelectorAll(".vehicle-card");
        const input = document.getElementById("selected_vehicle_id");
        const btn = document.getElementById("nextBtn");

        if (!cards.length || !input || !btn) return;

        cards.forEach(card => {
            card.addEventListener("click", function () {

                cards.forEach(c => c.classList.remove("selected"));
                this.classList.add("selected");

                if (this.dataset.id) {
                    input.value = this.dataset.id;
                    btn.disabled = false;
                }
            });
        });
    });

    /* =========================
       7. Counter Up
    ========================= */
    if ($.fn.counterUp) {
        $('[data-toggle="counter-up"]').counterUp({
            delay: 10,
            time: 2000
        });
    }

    /* =========================
       8. Back to Top Button
    ========================= */
    $(window).on("scroll", function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').on("click", function () {
        $('html, body').animate(
            { scrollTop: 0 },
            1500,
            'easeInOutExpo'
        );
        return false;
    });

    /* =========================
       9. Hero Background Slider
    ========================= */
    const slides = document.querySelectorAll(".carousel-slide");
    let currentSlide = 0;
    const slideInterval = 3000;

    function nextSlide() {
        if (!slides.length) return;

        slides[currentSlide].classList.remove("active");
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add("active");
    }

    if (slides.length > 1) {
        setInterval(nextSlide, slideInterval);
    }

})(jQuery);