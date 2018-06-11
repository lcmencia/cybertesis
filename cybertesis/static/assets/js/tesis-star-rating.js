/***
 * Contiene la valoración actual de la tesis
 * @type {number}
 */
var ratingValue = 0;


$(document).ready(function () {

    /* Inicializa pluging de rating*/
    $('#star-rating-holder').rating({
        captionElement: '#rating-caption-container',
        clearElement: '#rating-clear-container'
    });

    /* Cada vez que cambia valor de la valoración */
    $('#star-rating-holder').on('rating:change', function (event, value, caption) {
        ratingValue = value;
    });

    /* Cada vez que limpia la valoración */
    $('#star-rating-holder').on('rating:clear', function (event) {
        ratingValue = 0;
    });
});

/***
 * Se envían datos del formaulario de valoración de tesis
 * @param tesisId ID de la tesis
 */
function sendTesisRating(tesisId) {
    $("#ratingModal").modal('hide');
    $("#rating-star-container").hide();
    $("#rating-star-container-spinner").show();
    $.ajax({
        method: 'post',
        url: sendTesisRatingUrl,
        data: {
            csrfmiddlewaretoken: csrf,
            rate: ratingValue,
            tesis_id: tesisId,
            user_name: $("#user-name").val(),
            user_email: $("#user-email").val(),
        },
        success: function (data) {
            if('error_message' in data){
                var alertHtml = '<div class="alert alert-danger alert-dismissible">\n' +
                '    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\n' +
                '    <strong>¡Error!</strong> ' + data.error_message + '  </div>';
                $('#alert_placeholder').html(alertHtml)
            }else {
                var alertHtml = '<div class="alert alert-success alert-dismissible">\n' +
                    '    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\n' +
                    '    <strong>¡Exitoso!</strong> Su valoración fue registrada exitosamente.' +
                    '  </div>';
                var total_stars = 0
                if ("stars" in data) {
                    total_stars = parseInt(data.stars);
                    $("#rating-stars-value").text(data.stars + (total_stars == 1 ? ' estrella' : ' estrellas'));
                }
                if ("total_vote" in data) {
                    $("#rating-total-vote-value").text(data.total_vote + (parseInt(data.total_vote) == 1 ? ' voto' : ' votos'));
                }
                $('#alert_placeholder').html(alertHtml)
                var i;
                $("#stars-of-rating-container").html('');
                for (i = 0; i < total_stars; i++) {
                    $("#stars-of-rating-container").append('<i class="rating-stars filled-stars fa fa-star"></i>');
                }
                for (i = total_stars; i <= 5; i++) {
                    $("#stars-of-rating-container").append('<i class="rating-stars empty-stars fa fa-star-o"></i>');
                }
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            var alertHtml = '<div class="alert alert-danger alert-dismissible">\n' +
                '    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\n' +
                '    <strong>¡Error!</strong> ' +
                '  </div>';
            console.log("Status: " + textStatus);
            console.log("Error: " + errorThrown);
             $('#alert_placeholder').html(alertHtml)
        },
        complete: function () {
            $("#rating-star-container-spinner").hide();
            $("#rating-star-container").show();
            setTimeout(function () {
                $('html, body').animate({ scrollTop: 0 }, 'fast');
            }, 1000);
        }
    });

}