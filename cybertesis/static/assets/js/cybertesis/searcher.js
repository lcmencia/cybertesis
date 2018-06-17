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
            renderResultadosTesis(data.tesis_list, order);
            renderResultadosTutors(data.tutors_list);
            renderTopSearchedWords(data.top_words_searched);
            renderSearchStats(data.total_words, data.total_searchs);
            // Se agrega en el input el texto que buscó
            if(data.question){
                $("#buscador_principal").val(data.question);
            }
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

function renderResultadosTesis(data, order){
    $("#id-tesis-result-container").html(data);
    var navs = $("#id-tesis-result-container").find('.nav-link')
    var recent = navs[0];
    var rating = navs[1];
    if (order=='1'){
        rating.classList.remove("active");
        recent.classList.add("active");
    }else{
        recent.classList.remove("active");
        rating.classList.add("active");
    }
}

function renderResultadosTutors(data){
    // Genera la tabla de lista de tesis con los datos recibidos
    var $results_body = $("#recommend-tutors-body");
    $results_body.empty();
    for (var i = 0; i < data.length; i++) {
        var fields = data[i];
        var name = fields.name;
        var category = fields.category;
        var lastTutorial = fields.year;
        var newRowContent =
                    "<tr>" +
                        "<td>" + name + "</td>" +
                        "<td>" + category + "</td>" +
                        "<td>" + lastTutorial + "</td>" +
                    "</tr>";
        $results_body.append(newRowContent);
    }
}

function renderTopSearchedWords(wordsList){
    var $results_body = $("#id-table-top-searched-words");
    $results_body.empty();
    for (var i = 0; i < wordsList.length; i++) {
        var fields = wordsList[i];
        var word = fields.word;
        var count = fields.count;
        var newRowContent =
                    "<tr>" +
                        "<td>#" + (parseInt(i+1).toString()) + "</td>" +
                        "<td>" + word + "</td>" +
                        "<td>" + count + "</td>" +
                    "</tr>";
        $results_body.append(newRowContent);
    }
}

function renderSearchStats(total_words, total_searchs){
    $("#id-total-search").text(total_searchs);
    $("#id-total-searched-words").text(total_words);
}