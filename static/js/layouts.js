$(document).ready(function() {
    var select2 = $(".select2"), refresh_captcha = $('.js-captcha-refresh'),
        input_captcha = $('input[name="captcha_1"]'), input_fecha = $(".fecha"),
        file = $("#file"), form_upload = $('#form-upload-file');

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

    if (input_fecha.length) {
        var fecha = input_fecha.datepicker({
            format: 'dd/mm/yyyy'
        });
    }

    if (file.length && form_upload.length) {
        /** Accion a ejecutar al solicitar la descarga de archivos */
        $('.download-file').on('click', function(e) {
            e.preventDefault();
            set_filters();
        });

        /** realiza la accion de hacer click en el campo de archivo para cargar un archivo */
        $('.upload-file').on('click', function(e) {
            e.preventDefault();
            file.click();
        });

        /** Acciones a ejecutar al solicitar la carga de datos */
        file.on('change', function(e) {
            e.preventDefault();
            form_upload.ajaxForm({
                beforeSubmit: function(arr, $form, options) {
                    set_filters();
                },
                type: 'post',
                dataType: 'json',
                success: function(response) {
                    if (response.result) {
                        bootbox.alert(response.message);
                    }
                    else {
                        bootbox.alert(response.message);
                    }
                },
                error: function(jqxhr, textStatus, error) {
                    var err = textStatus + ", " + error;
                    bootbox.alert(MSG_PETICION_AJAX_FALLIDA + err);
                    console.log(MSG_PETICION_AJAX_FALLIDA + err);
                }
            }).submit();

            /** Previene el envio recurrente del formulario */
            form_upload.on('submit', function(e) {
                e.preventDefault();
            });

        });
    }
});