$(document).ready(function() {
    var $buscador_principal = $("#buscador_principal");
    var $buscador_principal_btn = $("#buscador_principal_btn");

    $buscador_principal_btn.on("click", function(){
        var search_text = $("#buscador_principal").val();
        ajax_search_text(search_text);
    });

    $buscador_principal.on("change keyup paste", function(){
        var search_text = $(this).val();
        ajax_search_text(search_text);
    });
});


function ajax_search_text(search_text){
    if (search_text.length > 2){
            $.ajax({
                url: searchUrl,
                type: 'GET',
                data: {
                    search_text: search_text
                },
                success: function(data){
                    console.log("DATA: " + data);
                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log(jqXHR);
                    console.log(textStatus);
                    console.log(errorThrown);
                },
                complete: function(result){
                    console.log("ALWAYS");
                },
            });
            console.log(search_text);
    }
}