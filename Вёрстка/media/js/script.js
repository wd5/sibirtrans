$(function() {
	$( "#price_filter_slider" ).slider({
		range: "min",
		value: 37,
		min: 5000,
		max: 200000,
		slide: function( event, ui ) {
			$( ".price_filter_input" ).val( ui.value );
		}
	});
	$( ".price_filter_input" ).val( $( "#price_filter_slider" ).slider( "value" ) );
});

$(function() {
	$( "#hotel_filter_slider" ).slider({
		range: "min",
		value: 1,
		min: 1,
		max: 5,
		step: 1
	});
});