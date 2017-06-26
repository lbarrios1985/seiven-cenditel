/**
 * @brief Función que permite descargar el archivo de carga masiva de datos
 * @param app Nombre de la aplicación de la cual se van a descargar los datos
 * @param mod Nombre del modelo que contiene el método de descarga de información
 * @param anho Año de registro del cual se van a descargar los datos. Este parámetro es opcional.
 * @param rel_id Identificador del modelo relacional del cual se van a descargar datos. Este parámetro es opcional.
 */
function cm_descargar_archivo(app, mod,filter) {
    var url_attrs = URL_DESCARGAR_ARCHIVO_CM+'?app=' + app + '&mod=' + mod + '&filter=' + filter;
    $(location).attr('href', url_attrs);
}

/**
 * @brief Función que realiza el procedimiento para la carga masiva de datos
 * @param app Nombre de la aplicación para la cual se van a cargar los datos
 * @param mod Nombre del modelo que contiene el método para la carga de datos
 * @param anho_id Identificador del elemento que contiene el año de registro
 * @param father_id Identificador del elemento relacionado al modelo
 * @param file Nombre del archivo que se va a cargar
 * @param form_token Cadena hash que contien el token del formulario a cargar
 */
function cm_cargar_archivo(app, mod,file, form_token) {
    var url_attrs = '?app=' + app + '&mod=' + mod ;
    var fdata = new FormData();
    fdata.append('file',file.files[0]);
    fdata.append('csrfmiddlewaretoken',form_token);
    $.ajax({
        url: URL_CARGAR_ARCHIVO_CM+url_attrs,
        data: fdata,
        contentType: false,
        processData: false,
        type: 'POST',
        dataType: 'json',
        success: function(data){
            var msg = data.result ? data.message : data.error;
            bootbox.alert(msg);
        },
        error: function(error){
            console.log(error);
        }
    });
}