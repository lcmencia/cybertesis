$(document).ready(function() {
    var $buscador_principal = $("#buscador_principal");
    var $buscador_principal_btn = $("#buscador_principal_btn");

    $buscador_principal_btn.on("click", function(){
        var search_text = $("#buscador_principal").val();
        ajax_search_text(search_text);
    });

//    $buscador_principal.on("change keyup paste", function(){
//        var search_text = $(this).val();
//        ajax_search_text(search_text);
//    });
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
                    var $results_body = $("#results_body");
                    $results_body.empty();
                    for(var i = 0; i < data.length; i++){
                        var fields = data[i].fields
                        var title = fields.title;
                        var year = fields.year;
                        var career = fields.career_name;
                        var faculty = fields.faculty_name;
                        var institution = fields.institution_name;

                        var newRowContent = "<tr><td style='text-overflow: ellipsis;'>"+title+"</td><td>"+career+"</td><td>"+
                            faculty+"</td><td>"+institution+"</td><td class='text-primary'>"+year+"</td></tr>";
                        $results_body.append(newRowContent);
                    }
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