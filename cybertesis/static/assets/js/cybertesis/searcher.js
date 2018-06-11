$(document).ready(function() {
    var $buscador_principal = $("#buscador_principal");
    var $buscador_principal_btn = $("#buscador_principal_btn");

    var $category_items = $(".category-item");
    $category_items.on("click", function(){
        // Por cada categoria en la lista de la izquierda, al hacer click sobre ella se filtran los resultados
        // Al realizar el click sobre una seleccionada, se elimina el filtro
        var active = $(this).hasClass("active");
        if (active){
            window.location = window.location.href.split("?")[0];
        }else{
            $(".category-item").removeClass("active");
            $(this).addClass("active");
            var id = this.id.split("_")[1];
            var href = document.location.href;
            if(href.indexOf("?") !== -1) {
                href = href.split("?")[0]
            }
            var url = href+"?category_id="+id;
            document.location = url;
        }
    });

    $buscador_principal_btn.on("click", function(){
        // Boton para realizar la busquedda
        var search_text = $("#buscador_principal").val();
        if (search_text.length > 2){
            ajax_search_text(search_text, 1);
        }
    });

    $buscador_principal.on("keyup", function(e){
        // Tecla enter en buscador principal ejecuta la busqueda
        if (e.keyCode == 13) {
            var search_text = $(this).val();
            if (search_text.length > 2){
                ajax_search_text(search_text, 1);
            }
        }
    });
});


function ajax_search_text(search_text, order){
    // Funcion para buscar una palabra y ordenar resultados
    data = {'order': order, 'search_text': search_text};
    var category_id = getUrlParameter('category_id');
    if (category_id != undefined){
        data['category_id'] = category_id;
    }

    $.ajax({
        url: searchUrl,
        type: 'GET',
        data: data,
        success: function(data){
            renderTable(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        },
        complete: function(result){
        },
    });
}

var getUrlParameter = function getUrlParameter(sParam) {
    // Obtiene el valor de un parametro en la url
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
    sURLVariables = sPageURL.split('&'),sParameterName,i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

function renderTable(data){
    // Genera la tabla de lista de tesis con los datos recibidos
    console.log("DATA: " + data);
    var $results_body = $("#results_body");
    $results_body.empty();
    for(var i = 0; i < data.length; i++){
        var fields = data[i].fields
        var title = fields.title;
        var year = fields.year;
        var career = fields.career_name;
        var faculty = fields.faculty_name;
        var institution = fields.institution_name;
        var id = fields.id;
        var rating = fields.rating;
        var newRowContent = "<tr><td><a href='/tesis/"+id+"/' target='_blank'>"+
                            "<span class='fa fa-external-link tesis-access-link'></span></a></td>"+
                            "<td style='text-overflow: ellipsis;'>"+title+"</td><td>"+career+"</td><td>"+
                            faculty+"</td><td>"+institution+"<td style='text-align: center;'>"+rating+
                            "<i class='rating-stars filled-stars fa fa-star'></i></td>"+
                            "</td><td class='text-primary'>"+year+"</td></tr>";
        $results_body.append(newRowContent);
    }
}