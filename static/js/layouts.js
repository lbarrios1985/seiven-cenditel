$(document).ready(function() {
    var select2 = $(".select2"), refresh_captcha = $('.js-captcha-refresh'),
        input_captcha = $('input[name="captcha_1"]');

    if (select2.length > 0) {
        select2.select2();
    }

    if (input_captcha.length) {
        /** Agrega clases de bootstrap para el input del captcha */
        input_captcha.addClass("form-control input-sm");

        /** Agrega un placeholder al input del captcha */
        input_captcha.attr("placeholder", "texto de la imagen");
    }

    if (refresh_captcha.length) {
        /** Actualiza la imagen captcha del formulario */
        refresh_captcha.click(function(){
            $form = $(this).parents('form');
            var url = location.protocol + "//" + window.location.hostname + ":" + location.port + "/captcha/refresh/";

            $.getJSON(url, {}, function(json) {
                $form.find('input[name="captcha_0"]').val(json.key);
                $form.find('img.captcha').attr('src', json.image_url);
            });

            return false;
        });
    }
});