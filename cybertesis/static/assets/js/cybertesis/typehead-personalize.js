$(document).ready(function () {
    var tesisSource = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('description'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: searchAutocompleteUrl,
            wildcard: '%QUERY',
            prepare: function (query, settings) {
                var category_id = getUrlParameter('category_id');
                var category_param = "";
                if (category_id != undefined){
                    category_param = "&category=" + category_id;
                }
                settings.url += '?q=' + $("#buscador_principal").val() + category_param;
                return settings;
            },
        }
    });
    tesisSource.initialize();
    $('#scrollable-dropdown-menu .typeahead').typeahead({
            hint: true,
            highlight: true,
            minLength: 3
        },
        {
            name: 'tesis',
            async: true,
            displayKey: 'title',
            value: 'title',
            source: tesisSource.ttAdapter(),
            limit: 10,
            templates: {
                empty: [
                    '<div class="empty-message">',
                    'No se encuentran referencias',
                    '</div>'
                ].join('\n'),
                header: '<h3 class="tesis-suggestions">Sugerencias:</h3>',
                suggestion: function (data) {
                    return '<p id="suggestion-tesis-' + data.tesis_id + '" class="d-inline-block text-truncate" style="max-width: 100%;">' +
                        '<span title="' + data.title + '"><strong>' + data.title + '</strong></span> - ' + data.description + '</p>';
                }
            }
        });

    $('.typeahead').bind('typeahead:select', function (ev, suggestion) {
        console.log('Selection: ' + suggestion);
        var val = $("#suggestion-tesis-" + suggestion.tesis_id).text();
        $("#buscador_principal").val(suggestion.title);
    });
    $('.typeahead').bind('typeahead:select', function (ev, suggestion) {
        console.log('Selection: ' + suggestion);
    });
});