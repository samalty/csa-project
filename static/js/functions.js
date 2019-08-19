
$(document).ready(function(){

    // Review form star rating system 
    $(".formStars").click(function(){
        $(this).css("color", "#cbab82");
        $(this).prevAll("label").css("color", "#cbab82");
        $(this).nextAll("label").css("color", "#e6e6e6");
    });

    // Scroll to top button
    $("#scrollTop").click(function(){
        $("html, body").animate({scrollTop: 0}, 500);
    });

});

// Scroll to top button visibility

var html, body, scrollTopBtn;

window.onload=function(){
    html=document.documentElement;
    body=document.body;
    scrollTopBtn=document.getElementById("scrollTop");
}

window.onscroll=scrollToTopAppear;

function scrollToTopAppear(){
    var windowInnerHeight=window.innerHeight;
    if (body.scrollTop > windowInnerHeight * 2 || html.scrollTop > windowInnerHeight * 2){
        scrollTopBtn.classList.add("visible");
    } else {
        scrollTopBtn.classList.remove("visible");
    }
}