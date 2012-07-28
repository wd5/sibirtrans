$(function() {
    $(".fancybox-thumb").fancybox({
        prevEffect	: 'none',
        nextEffect	: 'none',
        helpers	: {
            title	: {
                type: 'outside'
            },
            overlay	: {
                opacity : 0.8,
                css : {
                    'background-color' : '#000'
                }
            },
            thumbs	: {
                width	: 50,
                height	: 50
            }
        }
    });

    $('.fancybox').fancybox({helpers: {overlay : {opacity: 0.5}}});

    $('.tours_menu a').live('click', function() {
        $(this).parents(".tours_menu").find('li').removeClass('curr');
        $(this).parent().addClass('curr');

        $.ajax({
            url: "/load_tours/",
            data: {
                type:$(this).attr('name')
                //price_max:$('#price_filter_slider').slider( "option", "value" ),
                //star_max:$('#hotel_filter_slider').slider( "option", "value" )
            },
            type: "POST",
            success: function(data) {
                $('.item_first').remove();
                $('.items_catalog').replaceWith(data);

                var minp = $('#min_price').val()
                var maxp = $('#max_price').val()

                if ((minp==maxp) || (minp==undefined) || (maxp==undefined))
                    {
                        SetPriceSlider(0,0,minp);
                    }
                else
                    {
                        SetPriceSlider(parseInt(minp),parseInt(maxp),parseInt(maxp));
                    }

            },
            error:function(jqXHR,textStatus,errorThrown) {
                $('.catalog').replaceWith(jqXHR.responseText);
            }
        });

        return false;
    });

/*    $('.tour_other_hotels').jcarousel({
        scroll: 1,
        visible: 3,
        wrap: "circular"
    });*/

    //SlideTourImage();

	$( "#hotel_filter_slider" ).slider({
		range: "min",
		value: 1,
		min: 1,
		max: 5,
		step: 1,
        slide: function(event, ui) {

        },
        stop: function(event, ui) {
            var k = $(this).slider( "option", "value" )
            for (var i=1; i<6; ++i)
                {
                    if  (i<=k)
                        {
                            $('.star').eq(i-1).addClass('star_full');$('.star').eq(i-1).removeClass('star_empty')
                        }
                    else
                        {
                            $('.star').eq(i-1).addClass('star_empty');$('.star').eq(i-1).removeClass('star_full')
                        }
                }

            var val = $(this).slider( "option", "value" )
            var price_val = $('#price_filter_slider').slider( "option", "value" )
            $.ajax({
                url: "/load_tours/",
                data: {
                    type:$('.tours_menu li.curr a').attr('name'),
                    price_max:price_val,
                    max_star:val
                },
                type: "POST",
                success: function(data) {
                    $('.item_first').remove();
                    $('.items_catalog').replaceWith(data);
                },
                error:function(jqXHR,textStatus,errorThrown) {
                    $('.items_catalog').replaceWith(jqXHR.responseText);
                }
            });
        }
	});

    $('#send_question').live('click',function(){
        $.ajax({
            url: "/faq/checkform/",
            data: {
                question:$('#id_question').val(),
                email:$('#id_email').val()
            },
            type: "POST",
            success: function(data) {
                if (data=='success')
                    {
                        $('#result_text').html("Спасибо за вопрос, мы постараемся ответить на него в самое ближайшее время!");
                        $('#id_question').val("");
                        $('#id_email').val("");
                    }
                else{
                    $('.faq_form').replaceWith(data);
                }
            }
        });
        return false;
    });

    $('#send_order').live('click',function(){
        $.ajax({
            url: "/send_order/",
            data: {
                fullname:$('#id_fullname').val(),
                contacts:$('#id_contacts').val(),
                note:$('#id_note').val(),
                hotel:$('#id_hotel').val(),
                tour:$('#id_tour').val()
            },
            type: "POST",
            success: function(data) {
                if (data=='success')
                    {
                        $('.order_form').html("Заявка принята. Наш менеджер свяжется с вами в самое ближайшее время!");
                    }
                else{
                    $('.order_form').replaceWith(data);
                }
            }
        });
        return false;
    });

    $('.hotel_conditions_lnk a').toggle(
        function () {
            $('.hotel_condition_text').show('fast');
        },
        function () {
            $('.hotel_condition_text').hide('fast');
        }
    );

    $('.other_hotels_lnk a').toggle(
        function () {
            $('.tour_other_hotels_out').show();
            $('.tour_other_hotels').jcarousel({
                scroll: 1,
                visible: 3,
                wrap: "circular"
             });

        },
        function () {
            $('.tour_other_hotels_out').hide();
        }
    );

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

    $('.load_page a').live('click',function(){
        var el = $(this);
        var parent = $(this).parents('.load_block');
        var png_parent = $(this).parents('.load_page');
        $('.item_first').hide()

        //png_parent.find('.curr').removeClass('curr');
        //el.addClass('curr');

        $.ajax({
            url: "/load_items/",
            data: {
                load_ids: el.attr('name'),
                all_load_ids: $('#all_loaded_ids').val()
            },
            type: "POST",
            success: function(data) {
                //$('body,html,document').animate({scrollTop:500},"slow");
                parent.find('.item').remove()
                parent.find('.load_page').remove()
                parent.append(data)
                if ($('.load_page').find('a.curr').html()=='1')
                    {$('.item_first').show()}
                //parent.find('.loaded').show()  //простое появление
                //parent.find('div').removeClass('loaded')
            }
        });

        return false;

    });

});

function SetPriceSlider(min, max, start)
{

    $( "#price_filter_slider" ).slider({
		range: "min",
		value: start,
		min: min,
		max: max,
		slide: function( event, ui ) {
			$( ".price_filter_input" ).val( ui.value );
		},
        stop: function( event, ui ) {
            var val = $(this).slider( "option", "value" )
            $.ajax({
                url: "/load_tours/",
                data: {
                    type:$('.tours_menu li.curr a').attr('name'),
                    price_max:val
                },
                type: "POST",
                success: function(data) {
                    $('.item_first').remove();
                    $('.items_catalog').replaceWith(data);
                },
                error:function(jqXHR,textStatus,errorThrown) {
                    $('.items_catalog').replaceWith(jqXHR.responseText);
                }
            });
        }
	});
	$( ".price_filter_input" ).val( start );
}

/*
function SlideTourImage()
{
    var delay = 3000, fade = 1000; // tweak-able
    var imgs = $('.promo_img_slider');
    var map_imgs = $('.promo_map_slider');
    var len = imgs.length;
    var i = 0;

    setTimeout(cycle, delay); // <-- start

    function cycle() {
        $(imgs[i%len]).fadeOut(fade, function() {
            $(map_imgs[i%len]).fadeOut(fade, function() {
                $(map_imgs[i%len]).fadeIn(fade, function() {});
            });
            $(imgs[++i%len]).fadeIn(fade, function() { // mod ftw
                setTimeout(cycle, delay);
            });
        });
    }
}*/