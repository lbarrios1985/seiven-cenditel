/**
 * @brief Función que mide la fortaleza de la contraseña y la muestra en pantalla
 * @param password Cadena de carácteres con la contraseña indicada por el usuario
 */
function passwordStrength(password) {
    var desc = new Array();
    desc[0] = MSG_PASSWD_MUY_DEBIL;
    desc[1] = MSG_PASSWD_DEBIL;
    desc[2] = MSG_PASSWD_REGULAR;
    desc[3] = MSG_PASSWD_BUENA;
    desc[4] = MSG_PASSWD_FUERTE;
    desc[5] = MSG_PASSWD_MUY_FUERTE;

    var score = 0;

    //if password bigger than 6 give 1 point
    if (password.length > 6) score++;

    //if password has both lower and uppercase characters give 1 point
    if (( password.match(/[a-z]/) ) && ( password.match(/[A-Z]/) )) score++;

    //if password has at least one number give 1 point
    if (password.match(/\d+/)) score++;

    //if password has at least one special caracther give 1 point
    if (password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/)) score++;

    //if password bigger than 12 give another 1 point
    if (password.length > 12) score++;

    document.getElementById("passwordDescription").innerHTML = desc[score];
    document.getElementById("passwordStrength").className = "strength" + score;
    document.getElementById("passwordMeterId").value = score;
}

/**
 * @brief Funcion que permite mostrar u ocultar elementos con su id
 * @param element_id Cadena de texto con el id del elemento a mostrar u ocultar
 */
function show_hide(element_id) {
    $('.smal-box').each(function() {
        if (!$(this).is("#" + element_id)) {
            $(this).hide();
        }
    });
    var element = $("#" + element_id);

    //element.hide() ? element.is(":visible") : element.show();


    if (element.is(":visible")) {
        element.hide();
    }
    else {
        element.show();
    }
}

/**
 * @brief Funcion que permite mostrar los dominios indicados en
 * Balanza comercial
 * @param value Cadena de texto con el valor del select padre
 * @param element_id Cadena de texto con el id del elemento a modificar
 */
function edit_dom_bc(value,element_id) {
    if (value=='PR') {
        $('#'+element_id).html($('#balanza-comercial_completa').html());
        disable(element_id,false);
        disable('id_anho_base');
    }
    else if (value=='PC' || value =='PI') {
        $('#'+element_id).html($('#balanza-comercial_bs').html());
        disable(element_id,false);
        disable('id_anho_base',false);
    }
    else{
        disable(element_id);
        disable('id_anho_base');
    }
}

/**
 * @brief Funcion que permite mostrar los dominios indicados en
 * Balanza comercial
 * @param value Booleano para activar/desactivar el periodo
 */
function enable_periodo_bc(value) {
    if (value) {
        disable('id_periodo_trimestre_ini',false);
        disable('id_periodo_trimestre_fin',false);
        disable('id_periodo_anho_ini',false);
        disable('id_periodo_anho_fin',false);
    }
    else{
        disable('id_periodo_trimestre_ini');
        disable('id_periodo_trimestre_fin');
        disable('id_periodo_anho_ini');
        disable('id_periodo_anho_fin');
    }
}

/**
 * @brief Funcion que permite habilitar/deshabilitar elementos con su id
 * @param element_id Cadena de texto con el id del elemento a mostrar u ocultar
 * @param condicion Booleano que indica si el campo se debe deshabilitar o no
 */
function disable(element_id,condicion) {
    condicion = (typeof condicion != "undefined");
    var element = $("#" + element_id);
    if (condicion) {
        element.attr('disabled',true);
    }
    else {
        element.removeAttr('disabled');
    }
}

/**
 * @brief Funcion para validar los años y trimestres
 */
function validar_anho_trimestre() {
    trimestre_ini = $('#id_periodo_trimestre_ini').val();
    trimestre_fin = $('#id_periodo_trimestre_fin').val();
    anho_ini = $('#id_periodo_anho_ini').val();
    anho_fin = $('#id_periodo_anho_fin').val();
    if (trimestre_ini!='' &&  trimestre_fin!='' &&
        anho_ini!='' && anho_fin!='') {
        if (anho_fin<anho_ini) {
            return false
        }
        else if (anho_ini==anho_fin && trimestre_fin<=trimestre_ini) {
            return false
        }
        return true;
    }
}
