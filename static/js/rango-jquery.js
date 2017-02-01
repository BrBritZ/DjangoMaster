$(document).ready(function() {
    // JQuery code to be added in here.
    $("#about-btn").click(function(event)
    {
        alert("You clicked the button using JQuery!");

        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo"
        $("#msg").html(msgstr)
    });

    $("p").hover( function() {
        $(this).css('color', 'red');
        },
        function() {
            $(this).css('color', 'blue');
    });

    $(".rango-add").click(function(){
        var catid = $(this).attr("data-catid");
        var url = $(this).attr("data-url");
        var title = $(this).attr("data-title");
        var me = $(this)
        $.get('/rango/add/',
            {category_id: catid, url: url, title: title}, function(data){
                $("#pages").html(data);
                me.hide();
            });
    });

});