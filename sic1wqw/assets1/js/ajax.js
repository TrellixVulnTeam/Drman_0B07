//$(document).ready(function(){
//    $(function() {
//                    // perform search on page load
//                    alert("ohh");
//                    search();
//                    $('#search').keyup(search);
//
//                });
//
//                function searchSuccess(data , textStatus , jqXHR) {
//                    $('#search-results').html(data) ;
//                };
//
//                function search() {
//                    $.ajax({
//                                type: "POST",
//                                url: "/doctors/ajax_search/",
//                                data: {
//                                    'search_text' : $('#search').val(),
//                                    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
//                                    } ,
//                                success: searchSuccess ,
//                                error: function(xhr) {
//                                    alert("err");
//                                } ,
//                                dataType : 'html'
//                    });
//                }
//
//}
//
//////$(document).ready(function(){
//////				 $('select#selectcountries').change(function () {
//////    				 var optionSelected = $(this).find("option:selected");
//////    				 var valueSelected  = optionSelected.val();
//////     				 var country_name   = optionSelected.text();
//////                     alert(country_name);
//////     				 data = {'cnt' : country_name };
//////       				 var req = ajax('/doctors/getdetails/',data,function(result){
//////       					 	alert(result);
//////       					 	$("#selectcities option").remove();
//////       					 	for (var i = result.length - 1; i >= 0; i--) {
//////       					 		$("#selectcities").append('<option>'+ result[i] +'</option>');
//////       					 	};
//////
//////       					 });
//////
////// 				 });
//////			});
////
////
////$(document).ready(function(){
////$('select#selectcountries').change(function () {
////           var optionSelected = $(this).find("option:selected");
////    				 var valueSelected  = optionSelected.val();
////     				 var country_name   = optionSelected.text();
////                     alert(country_name);
////
////          $.ajax({
////            url: '/doctors/ajax_search/',                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
////            data: {'cnt' : country_name,
////
////            },
////            success: function (data, textStatus , jqXHR) {   // `data` is the return of the `load_cities` view function
////            alert(data);
//////            $("#selectcities option").remove();
////              $('#search-results').html(data) ;
////
////            } ,
////            error: function(xhr) {
////                                    alert("err");
////                                } ,
////            dataType : 'html'
////          });
////
////        });
////        });

//<!--<script>-->
//      <!--$(function() {-->
//
//
//
//    <!--function searchSuccess(data) {-->
//
//            <!--var availableTags = [-->
//      <!--"ActionScript",-->
//      <!--"AppleScript",-->
//      <!--"Asp",-->
//      <!--"BASIC",-->
//      <!--"C",-->
//      <!--"C++",-->
//      <!--"Clojure",-->
//      <!--"COBOL",-->
//      <!--"ColdFusion",-->
//      <!--"Erlang",-->
//      <!--"Fortran",-->
//      <!--"Groovy",-->
//      <!--"Haskell",-->
//      <!--"Java",-->
//      <!--"JavaScript",-->
//      <!--"Lisp",-->
//      <!--"Perl",-->
//      <!--"PHP",-->
//      <!--"Python",-->
//      <!--"Ruby",-->
//      <!--"Scala",-->
//      <!--"Scheme"-->
//    <!--];-->
//
//    <!--&lt;!&ndash;alert(data);&ndash;&gt;-->
//
//        <!--$.each(availableTags, function(index, value){-->
//
//                    <!--t = response(value);-->
//
//
//                <!--});-->
//
//
//
//
//<!--}-->
//
//    <!--$( "#ajab" ).autocomplete({-->
//      <!--source: function( request, response ) {-->
//            <!--$.ajax({-->
//              <!--type: "POST",-->
//              <!--url: "/doctors/ajax_search/",-->
//              <!--dataType: "json",-->
//              <!--data: {-->
//                                        <!--'search_text' : $('#ajab').val(),-->
//                                        <!--'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()-->
//                                        <!--} ,-->
//              <!--success: searchSuccess ,-->
//            <!--});-->
//      <!--},-->
//      <!--select: function (){-->
//          <!--console.log('select');-->
//      <!--}-->
//    <!--}).val('ActionScript').data('autocomplete')._trigger('select');-->
//  <!--});-->
//<!--</script>-->
//<!--<script>-->
//
//<!--function searchSuccess(data) {-->
//    <!--alert(data);-->
//
//    <!--var m = response($.map(data, function (item) {-->
//            <!--alert(item);-->
//            <!--return {-->
//
//                <!--value: item-->
//            <!--};-->
//
//        <!--}));-->
//
//    <!--alert("baddd");-->
//
//<!--}-->
//  <!--$(function() {-->
//    <!--function log( message ) {-->
//      <!--$( "<div>" ).text( message ).prependTo( "#log" );-->
//      <!--$( "#log" ).scrollTop( 0 );-->
//    <!--}-->
//
//    <!--$( "#ajab" ).autocomplete({-->
//      <!--source: function( request, response ) {-->
//        <!--$.ajax({-->
//          <!--type: "POST",-->
//          <!--url: "/doctors/ajax_search/",-->
//          <!--dataType: "json",-->
//          <!--data: {-->
//                                    <!--'search_text' : $('#ajab').val(),-->
//                                    <!--'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()-->
//                                    <!--} ,-->
//          <!--success: searchSuccess ,-->
//        <!--});-->
//      <!--},-->
//      <!--minLength: 3,-->
//      <!--select: function( event, ui ) {-->
//        <!--log( ui.item ?-->
//          <!--"Selected: " + ui.item :-->
//          <!--"Nothing selected, input was " + this.value);-->
//      <!--},-->
//      <!--open: function() {-->
//        <!--$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );-->
//      <!--},-->
//      <!--close: function() {-->
//        <!--$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );-->
//      <!--}-->
//    <!--});-->
//  <!--});-->
//<!--</script>-->