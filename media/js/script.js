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

    $('.contacts_city a').toggle(function() {
        $('.contacts_city_menu').show();
    }, function() {
        $('.contacts_city_menu').hide();
    });

    $('.contacts_city_menu a').live('click',function(){
        var el = $(this)
        var parent = el.parent()
        $('.contacts_city_menu').hide();
        parent.parent().prepend('<li><a href="#">' + $('.city_curr').html() +
            '</a><span class="tel" style="display: none;">' + $('div.tel').html() +
            '</span><span class="city_in" style="display: none;">' + $('.contacts_city a span').html() + '</span></li>')
        $('.city_curr').html(el.html())
        $('div.tel').html(parent.find('.tel').html())
        $('.contacts_city a span').html(parent.find('.city_in').html())
        parent.remove()
        $.ajax({
            type:'post',
            url:'/set_cookie_contact_id/',
            data:{
                'st_contact_city':el.html()
            },
            success:function(data){
            },
            error:function(data){
            }
        });
        return false;
    });

});