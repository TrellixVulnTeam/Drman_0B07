//Ready function when page is loaded
$(document).ready(function() {
    //Autocomplete function
    var autoCompleteDemo = function(query, cb) {
        var results = $.map([0], function() {
            //Get text from the input field
            var text = document.getElementById('typeahead').value;
            //ES Query
            var json = {
                publication : {
                    text : text,
                    completion : {
                        field : "title_suggest"
                    }
                }
            };
            
            //Ajax call to ES make sure this matches YOUR ES info
            var request = $.ajax({
                type : "POST",
                url : "http://elasticsearch613:9200/doctor/_search",
                async : false,
                data : JSON.stringify(json),
                contentType : "application/json; charset=utf-8",
                dataType : "json",
                success : function(data) {
                    return (data);
                },
                failure : function(errMsg) {
                    alert(errMsg);
                }
            });
            
            //Parse the results and return them
            var response = JSON.parse(request.responseText);
            var resultsArray = response.publication[0].options;
            var datum = [];
            for (var i = 0; i < resultsArray.length; i++) {
                datum.push({
                    theValue : resultsArray[i].text
                });
            }
            return datum;
        });

        cb(results);
    };

    $('.typeahead').typeahead(null, {
        displayKey : 'theValue',
        source : autoCompleteDemo
    });

}); 