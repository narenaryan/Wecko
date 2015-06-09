

$( ".target" ).change(function() {

var country = $( ".target" ).val();

$.get( "/cmap/" + country, function( data ) {
  console.log("success");

});
});

