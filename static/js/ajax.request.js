/**
 * @brief Función que permite la descarga de archivos para la gestión de información
 * @param url ['string] Contiene la URL para la descargar de archivos de gestión de información
 * @param app [string] Contiene el nombre de la aplicación o módulo para la gestión de los datos
 * @param mod ['string'] Contiene el nombre del modelo del cual descargará los datos
 * @param filter ['string'] Contiene el filtro a aplicar en la búsqueda de información para generar el archivo
 */
function descargar_archivo(url, app, mod, filter) {
    params = (typeof(filter)!="undefined") ? {app:app, mod:mod, filter: filter} : {app:app, mod:mod};

    $.getJSON(url, params, function(datos) {
        if (datos.resultado) {
            bootbox.alert(datos.message);
            window.open(URL_STATIC_INFO_FILES+datos.archivo);
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        console.log(MSG_PETICION_AJAX_FALLIDA + err)
    });
}


/**
 * @brief Función que permite la carga de datos en el sistema
 * @param url ['string] Contiene la URL para la cargar de datos
 * @param app [string] Contiene el nombre de la aplicación o módulo para registrar los datos
 * @param mod ['string'] Contiene el nombre del modelo en el cual se cargarán los datos
 * @param filter ['string'] Contiene el filtro a aplicar en el registro de datos
 */
function cargar_archivo(url, app, mod, filter) {
    params = (typeof(filter)!="undefined") ? {app:app, mod:mod, filter: filter} : {app:app, mod:mod};

    $.getJSON(url, params, function(datos) {
        if (datos.resultado) {
            bootbox.alert(datos.message);
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( MSG_PETICION_AJAX_FALLIDA + err );
        console.log(MSG_PETICION_AJAX_FALLIDA + err)
    });
}