/**
 * @brief Función que permite la descarga de archivos para la gestión de información
 * @param url ['string] Contiene la URL para la descargar de archivos de gestión de información
 * @param app [string] Contiene el nombre de la aplicación o módulo para la gestión de los datos
 * @param mod ['string'] Contiene el nombre del modelo del cual descargará los datos
 */
function descargar_archivo(url, app, mod) {

    $.getJSON(url, {app:app, mod:mod}, function(datos) {
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