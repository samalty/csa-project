// Review form star rating system 

$(document).ready(function(){
    $(".formStars").click(function(){
        $(this).css("color", "#ffd11a");
        $(this).prevAll("label").css("color", "#ffd11a");
        $(this).nextAll("label").css("color", "#e6e6e6");
    });
});