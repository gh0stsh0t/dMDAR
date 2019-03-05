window.onload = function() {
    const r1 = new JSR(['#range-2-1', '#range-2-2'], {
        sliders: 2,
        min: 0,
        max: 5,
        step: 0.5,
        values: [0, 5],
        limit: {
            show: false
        },
        labels: {
            formatter: (value) => {
                return value.toString();
            }
        }
    }).setLimit('min', 0).setLimit('max', 5);
    setTimeout(() => {
        r1.refresh({
            min: 0,
            limit: {
                min: 0,
                max: 5
            }
        });
    }, 2000);
    r1.addEventListener('update', (input, value) => {
        $('first-star-filter').val(value);
        $('second-star-filter').val(value);
    });
    const r2 = new JSR(['#range-2-1a', '#range-2-2a'], {
        sliders: 2,
        min: 0,
        max: 5,
        step: 0.5,
        values: [0, 5],
        limit: {
            show: false
        },
        labels: {
            formatter: (value) => {
                return value.toString();
            }
        }
    }).setLimit('min', 0).setLimit('max', 5);
    setTimeout(() => {
        r2.refresh({
            min: 0,
            limit: {
                min: 0,
                max: 5
            }
        });
    }, 2000);
};



$(function () {
    $(window).on("scroll", function () {
        if ($("#navbarSupportedContent").hasClass("show")){
            $('.navbar-toggler').click();
        }
        if ($(window).scrollTop() > (window.innerHeight - 100)) {
            $("#nav-bar").addClass("navigation-bar-color");
        } else {
            //remove the background property so it comes transparent again (defined in your css)
            $("#nav-bar").removeClass("navigation-bar-color");
        }
    });
    $(window).on("scroll", function () {
        if ($("#navbarSupportedContent").hasClass("show")){
            $('.navbar-toggler').click();
        }
        if ($(window).scrollTop() > 10) {
            $("#nav-bar-normal").addClass("navigation-bar-color");
        } else {
            //remove the background property so it comes transparent again (defined in your css)
            $("#nav-bar-normal").removeClass("navigation-bar-color");
        }
    });
    $("#openSearch").on("click", function () {
        if ($("#nav-bar-normal, #nav-bar").hasClass("nav-search-active") && $("#search").val() == "" && !$("#navbarSupportedContent").hasClass("show")){
            $("#nav-bar-normal, #nav-bar").removeClass("nav-search-active");
        } else {
            $("#nav-bar-normal, #nav-bar").addClass("nav-search-active");
        }
    });
    $("#openSearch").on("mouseover", function () {
        if ($("#nav-bar-normal, #nav-bar").hasClass("nav-search-active") && $("#search").val() == "" && !$("#navbarSupportedContent").hasClass("show")){
            $("#nav-bar-normal, #nav-bar").removeClass("nav-search-active");
        } else {
            $("#nav-bar-normal, #nav-bar").addClass("nav-search-active");
        }
    });
    $("#search").on("mouseleave", function () {
        if(!$("#search").is(":focus") && $("#search").val() == "" && !$("#navbarSupportedContent").hasClass("show")){
            $("#nav-bar-normal, #nav-bar").removeClass("nav-search-active");
        }
    });
    $("#search").on("focusout", function () {
        if($("#search").val() == "" && !$("#navbarSupportedContent").hasClass("show")){
            $("#nav-bar-normal, #nav-bar").removeClass("nav-search-active");
        }
    });
    $("#nav-toggle").on("click", function () {
        if (!$("#navbarSupportedContent").hasClass("show")){
            $("#nav-bar-normal, #nav-bar").addClass("nav-search-active navigation-bar-color navigation-bar-show ");
            $("#openSearch").hide();
        } else {
            $("#nav-bar-normal, #nav-bar").removeClass("nav-search-active navigation-bar-color navigation-bar-show ");
            $("#openSearch").show();
        }
    });

    var starRating = 0;
    $("#write-review-star1").on("mouseenter", function () {
        $("#write-review-star1").addClass("checked");
        $("#write-review-star2").removeClass("checked");
        $("#write-review-star3").removeClass("checked");
        $("#write-review-star4").removeClass("checked");
        $("#write-review-star5").removeClass("checked");
    });
    $("#write-review-star1").on("click", function () {
        if (!$("#write-review-star1").hasClass("selected")) $("#write-review-star1").addClass("selected");
        if ($("#write-review-star2").hasClass("selected")) $("#write-review-star2").removeClass("selected");
        if ($("#write-review-star3").hasClass("selected")) $("#write-review-star3").removeClass("selected");
        if ($("#write-review-star4").hasClass("selected")) $("#write-review-star4").removeClass("selected");
        if ($("#write-review-star5").hasClass("selected")) $("#write-review-star5").removeClass("selected");
        starRating = 1;
    });
    $("#write-review-star2").on("mouseenter", function () {
        $("#write-review-star1").addClass("checked");
        $("#write-review-star2").addClass("checked");
        $("#write-review-star3").removeClass("checked");
        $("#write-review-star4").removeClass("checked");
        $("#write-review-star5").removeClass("checked");
    });
    $("#write-review-star2").on("click", function () {
        if (!$("#write-review-star1").hasClass("selected")) $("#write-review-star1").addClass("selected");
        if (!$("#write-review-star2").hasClass("selected")) $("#write-review-star2").addClass("selected");
        if ($("#write-review-star3").hasClass("selected")) $("#write-review-star3").removeClass("selected");
        if ($("#write-review-star4").hasClass("selected")) $("#write-review-star4").removeClass("selected");
        if ($("#write-review-star5").hasClass("selected")) $("#write-review-star5").removeClass("selected");
        starRating = 2;
    });
    $("#write-review-star3").on("mouseenter", function () {
        $("#write-review-star1").addClass("checked");
        $("#write-review-star2").addClass("checked");
        $("#write-review-star3").addClass("checked");
        $("#write-review-star4").removeClass("checked");
        $("#write-review-star5").removeClass("checked");
    });
    $("#write-review-star3").on("click", function () {
        if (!$("#write-review-star1").hasClass("selected")) $("#write-review-star1").addClass("selected");
        if (!$("#write-review-star2").hasClass("selected")) $("#write-review-star2").addClass("selected");
        if (!$("#write-review-star3").hasClass("selected")) $("#write-review-star3").addClass("selected");
        if ($("#write-review-star4").hasClass("selected")) $("#write-review-star4").removeClass("selected");
        if ($("#write-review-star5").hasClass("selected")) $("#write-review-star5").removeClass("selected");
        starRating = 3;
    });
    $("#write-review-star4").on("mouseenter", function () {
        $("#write-review-star1").addClass("checked");
        $("#write-review-star2").addClass("checked");
        $("#write-review-star3").addClass("checked");
        $("#write-review-star4").addClass("checked");
        $("#write-review-star5").removeClass("checked");
    });
    $("#write-review-star4").on("click", function () {
        if (!$("#write-review-star1").hasClass("selected")) $("#write-review-star1").addClass("selected");
        if (!$("#write-review-star2").hasClass("selected")) $("#write-review-star2").addClass("selected");
        if (!$("#write-review-star3").hasClass("selected")) $("#write-review-star3").addClass("selected");
        if (!$("#write-review-star4").hasClass("selected")) $("#write-review-star4").addClass("selected");
        if ($("#write-review-star5").hasClass("selected")) $("#write-review-star5").removeClass("selected");
        starRating = 4;
    });
    $("#write-review-star5").on("mouseenter", function () {
        $("#write-review-star1").addClass("checked");
        $("#write-review-star2").addClass("checked");
        $("#write-review-star3").addClass("checked");
        $("#write-review-star4").addClass("checked");
        $("#write-review-star5").addClass("checked");
    });
    $("#write-review-star5").on("click", function () {
        if (!$("#write-review-star1").hasClass("selected")) $("#write-review-star1").addClass("selected");
        if (!$("#write-review-star2").hasClass("selected")) $("#write-review-star2").addClass("selected");
        if (!$("#write-review-star3").hasClass("selected")) $("#write-review-star3").addClass("selected");
        if (!$("#write-review-star4").hasClass("selected")) $("#write-review-star4").addClass("selected");
        if (!$("#write-review-star5").hasClass("selected")) $("#write-review-star5").addClass("selected");
        starRating = 5;
    });
    $("#write-review-star-group").on("mouseleave", function () {
        if (!$("#write-review-star1").hasClass("selected")) $("#write-review-star1").removeClass("checked");
        else $("#write-review-star1").addClass("checked");
    
        if (!$("#write-review-star2").hasClass("selected")) $("#write-review-star2").removeClass("checked");
        else $("#write-review-star2").addClass("checked");

        if (!$("#write-review-star3").hasClass("selected")) $("#write-review-star3").removeClass("checked");
        else $("#write-review-star3").addClass("checked");

        if (!$("#write-review-star4").hasClass("selected")) $("#write-review-star4").removeClass("checked");
        else $("#write-review-star4").addClass("checked");

        if (!$("#write-review-star5").hasClass("selected")) $("#write-review-star5").removeClass("checked");
        else $("#write-review-star5").addClass("checked");
    });
    $('#user-reviews-table tr').hover(function() {
        $(this).addClass('user-reviews-actions-show');
    }, function() {
        $(this).removeClass('user-reviews-actions-show');
    });

});


(function() {
    function scrollHorizontally(e) {
        e = window.event || e;
        var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
        document.getElementById('scrollId').scrollLeft -= (delta*40); // Multiplied by 40
        e.preventDefault();
    }
    if (document.getElementById('scrollId').addEventListener) {
        // IE9, Chrome, Safari, Opera
        document.getElementById('scrollId').addEventListener("mousewheel", scrollHorizontally, false);
        // Firefox
        document.getElementById('scrollId').addEventListener("DOMMouseScroll", scrollHorizontally, false);
    } else {
        // IE 6/7/8
        document.getElementById('scrollId').attachEvent("onmousewheel", scrollHorizontally);
    }
})();

(function() {
    function scrollHorizontally(e) {
        e = window.event || e;
        var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
        document.getElementById('scrollId2').scrollLeft -= (delta*40); // Multiplied by 40
        e.preventDefault();
    }
    if (document.getElementById('scrollId2').addEventListener) {
        // IE9, Chrome, Safari, Opera
        document.getElementById('scrollId2').addEventListener("mousewheel", scrollHorizontally, false);
        // Firefox
        document.getElementById('scrollId2').addEventListener("DOMMouseScroll", scrollHorizontally, false);
    } else {
        // IE 6/7/8
        document.getElementById('scrollId2').attachEvent("onmousewheel", scrollHorizontally);
    }
})();

(function() {
    function scrollHorizontally(e) {
        e = window.event || e;
        var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
        document.getElementById('scrollId3').scrollLeft -= (delta*40); // Multiplied by 40
        e.preventDefault();
    }
    if (document.getElementById('scrollId3').addEventListener) {
        // IE9, Chrome, Safari, Opera
        document.getElementById('scrollId3').addEventListener("mousewheel", scrollHorizontally, false);
        // Firefox
        document.getElementById('scrollId3').addEventListener("DOMMouseScroll", scrollHorizontally, false);
    } else {
        // IE 6/7/8
        document.getElementById('scrollId3').attachEvent("onmousewheel", scrollHorizontally);
    }
})();

function showEditReview(id){
    $("#edit-review-modal").modal({
        backdrop: 'static',
        keyboard: false
    })
}

function archiveReview(id) {
    alert(id);
}

// OWN SCRIPTS

// login module
$('#login-form .form-control').keypress(function(e){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13') { // check if enter key is pressed
        $('#login-form').trigger('submit');
    }
});

$('#login-form').submit(function(e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: 'login',
        data: $(this).serialize(),
        success: function(data) {
            if(data.fail) {
                $('.invalid-feedback').show();
                $('#exampleDropdownFormPassword1').addClass('is-invalid');
            }
            else {
                location.reload();
            }
        },
        error: function(data) {

        }
    });
});

// filter catalogs page
var filterTimer;
var filterInterval = 250;
$('#drop-sort, #drop-num-results').change(function() {
    console.log("dropdown filter");
    clearTimeout(filterTimer);
    filter();
    filterTimer = setTimeout(filter, filterInterval);
});

$(document).on('change', '.form-check-input', function() {
    console.log("test");
});

function filter() {
    // $.ajax({
    //     type: 'POST',
    //     url: 'catalog',
    //     data: 
    //     success: function(data) {
            
    //     }
    // });
}