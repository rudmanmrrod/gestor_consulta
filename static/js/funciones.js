/**
 * Función para agregar preguntas en la consulta
 * @param element Recibe nombre de elemento a agregar
**/
function agregar_preguntas(element) {
    $('#agregar_preguntas').append($(element).html());
    $('select').formSelect();
}

/**
 * Función para eliminar preguntas agregadas dinámicamente
 * @param element Recibe el elemento a partir del cual se eliminará la fila
**/
function eliminar_preguntas(element) {
    $(element).parent().parent().remove();
}

/**
 * Función para validar las preguntas agregadas dinámicamente
 * @param event Recibe el evento click
**/
function validar_preguntas(event) {
    var longitud = $('#agregar_preguntas').find('.row');
    if(longitud.length>0)
    {
        var vacio = false;
        $.each(longitud.find('input'),function(key,value){
            if ($(value).val().trim()=='') {
                vacio = true;
            }
        });
        $.each(longitud.find('select'),function(key,value){
            if ($(value).val().trim()=='') {
                vacio = true;
            }
        });
        if (vacio) {
            event.preventDefault();
            bootbox.dialog({
                message: "Debe llenar todas las preguntas que agregó",
                title: "<b class='text-danger'>Error</b>",
                buttons: {
                    success: {
                        label: "Cerrar",
                        className: "btn-danger",
                        callback: function() {}
                    }
                }
            });
        }
    }
}

/**
 * Función para cargar preguntas luego de un error en el formulario
**/
function cargar_preguntas() {
    $.each(opciones,function(){
        $('#agregar_preguntas').append($('#preguntas').html());    
    });
    $.each($('#agregar_preguntas #id_texto_pregunta_modal'),function(key,value){
        $(value).val(opciones[key]['texto_pregunta']);
    });
    $.each($('#agregar_preguntas #id_tipo_pregunta_modal'),function(key,value){
        $(value).val(opciones[key]['tipo_pregunta']).change();
    });
}

/**
 * Función para agregar opciones si la pregunta lo requiere
 * @param element Recibe el elemento de la consulta
**/
function add_option(element) {
    var option = $(element).parent().parent().parent().find('#for_options');
    $(option).append($('#agregar_opciones').html());
}

/**
 * Función para agregar opciones si la pregunta lo requiere
 * @param element Recibe el id de la consulta
**/
function remove_option(element) {
    $(element).parent().remove();
}

/**
 * Función para mostrar las preguntas de una consulta
 * @param id Recibe el id de la consulta
**/
function ver_preguntas(id) {
    $.ajax({
        type: 'GET',
        url: URL_LISTAR_PREGUNTAS+id,
        success: function(response) {
            if (response.success) {
                var preguntas = response.preguntas;
                var token = $('input').val();
                var html = '<form action="" role="form" method="post" id="question_form">';
                html += '<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'">';
                $.each(preguntas,function(key,value){
                    html += "<div><h4>Pregunta #"+parseInt(key+1)+"</h4>";
                    html+= $('#preguntas').html();
                    html += "<hr></div>";
                });
                MaterialDialog.dialog(
                    html,
                    {
                        title:"",
                        buttons:{
                            close:{
                                className:"deep-orange lighten-1",
                                text:"Cerrar",
                            },
                            confirm:{
                                className:"deep-orange lighten-1",
                                text:"Guardar",
                                callback:function(){
                                    update_question();
                                }
                            }
                        }
                    }
                );
                $.each($('.material-dialog').last().find('.modal-content #id_texto_pregunta_modal'),function(key,value){
                    $(value).val(preguntas[key]['texto_pregunta']);
                    $(value).append('<input type="hidden" name="texto_pregunta_id" value="'+preguntas[key]['id']+'">');
                });
                $.each($('.material-dialog').last().find('.modal-content select'),function(key,value){
                    $(value).val(preguntas[key]['tipo_pregunta']).change();
                    if (preguntas[key]['tipo_pregunta']<=2) {
                        var padre = $(value).parent().parent();
                        var agregar_opciones = $(padre).find("#add_options");
                        html = '<div class="col m6">'
                        html += '<a class="deep-orange-text lighten-1" href="#" onclick="agregar_opcion('+preguntas[key]['id']+')">';
                        html += '<h6>Agregar opción <i class="tiny material-icons left">add_circle_outline</i></h6></a></div>';
                        html += '<div class="col m6">'
                        html += '<a class="deep-orange-text lighten-1" href="#" onclick="see_option('+preguntas[key]['id']+')">';
                        html += '<h6>Ver opciones <i class="material-icons left">search</i></h6></a></div>';
                        $(padre).append(html);
                    }
                });
                $.each($('.material-dialog').last().find('.modal-content span a'),function(key,value){
                    $(value).attr('onclick','del_pregunta('+preguntas[key]['id']+')');
                });
                $('select').material_select();
            }
            else{
                
            }
        },
        error:function(error)
        {
            M.toast({html:"Ocurrió un error inesperado"});
        }
    });
}

/**
 * Función para abrir el formulario de opciones
 * @param id Recibe el id de la pregunta
**/
function agregar_opcion(id) {
    MaterialDialog.dialog(
        $('#formulario').html(),
        {
            title:"Opciones",
            modalType:"bottom-sheet",
            buttons:{
                close:{
                    className:"deep-orange lighten-1",
                    text:"Cerrar",
                },
                confirm:{
                    className:"deep-orange lighten-1",
                    text:"Guardar",
                    callback:function(){
                        submitOption($('.material-dialog #formulario_modal').last());
                    }
                }
            }
        }
    );
    $('.material-dialog').last().find('#formulario_modal').append($('#agregar_opciones_base').html());
    $('.material-dialog').last().find('#formulario_modal').attr('action',id);
}

/**
 * Función para enviar el formulario de las opciones
 * @param objecto Recibe el objecto
**/
function submitOption(objecto) {
    var input = $(objecto).find('#opciones #id_texto_opcion');
    var vacio = false;
    $.each(input,function(key,value){
        if ($(value).val().trim()=='') {
            vacio = true;
        }
    });
    if (!vacio) {
        $.ajax({
            data: $(objecto).serialize(), 
            type: 'POST',
            url: URL_CREAR_OPCIONES+$(objecto).attr('action'),
            success: function(response) {
                if (response.code) {
                    M.toast({html:'Se crearon las opciones con éxito'});
                }
                else{
                    var errors = '';
                    $.each(response.errors,function(key,value){
                        errors += key+" "+value+"<br>";
                    });
                    M.toast({hmtl:errors});
                }
            }
        });
    }
    else{
        M.toast({html:'Debe llenar todas las opciones'});
    }
}

/**
 * Función para ver las opciones de un pregunta
 * @param id Recibe el id de la pregunta
**/
function see_option(id) {
    $.ajax({
    type: 'GET',
    url: URL_LISTAR_OPCIONES+id,
    success: function(response) {
        if (response.success) {
            var opciones = response.opciones;
            var token = $('input').val();
            var html = '<form action="" role="form" method="post" id="option_form">';
            html += '<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'">';
            $.each(opciones,function(key,value){
                html += "<div><h4>Opcion #"+parseInt(key+1)+"</h4>";
                html+= $('#agregar_opciones').html();
                html += "<hr></div>";
            });
            html+= '</form>';
            MaterialDialog.dialog(
                html,
                {
                    title:"Opciones",
                    modalType:"bottom-sheet",
                    buttons:{
                        close:{
                            className:"deep-orange lighten-1",
                            text:"Cerrar",
                        },
                        confirm:{
                            className:"deep-orange lighten-1",
                            text:"Guardar",
                            modalClose:false,
                            callback:function(){
                                update_option(id);
                            }
                        }
                    }
                }
            );
            $.each($('.material-dialog').last().find('.modal-content #option_form #id_texto_opcion'),function(key,value){
                $(value).val(opciones[key]['texto_opcion']);
                $(value).append('<input type="hidden" name="texto_opcion_id" value="'+opciones[key]['id']+'">');
            });
            $.each($('.material-dialog').last().find('.modal-content #option_form #opciones a'),function(key,value){
                $(value).attr('onclick','del_option(this,'+opciones[key]['id']+')');
            });
            }
        },
        error:function(error)
        {
            M.toast({hmtl:"Ocurrió un error inesperado"});
        }
    });
}

/**
 * Función para actualizar las opciones de un pregunta
 * @param id Recibe el id de la pregunta
**/
function update_option(id) {
    var form = $('.material-dialog').last().find("#option_form");
    $.ajax({
        data: $(form).serialize(), 
        type: 'POST',
        url: URL_ACTUALIZAR_OPCIONES,
        success: function(response) {
            if (response.code) {
                M.toast({html:"Se actualizaron las opciones con éxito"});
            }
            else{
                var errors = '';
                $.each(response.errors,function(key,value){
                    errors += key+" "+value+"<br>";
                });
                M.toast({html:errors});
            }
        }
    }); 
}

/**
 * Función para eliminar las opciones de un pregunta
 * @param id Recibe el id de la pregunta
**/
function del_option(objeto,id) {
    MaterialDialog.dialog(
        "¿Desea borrar la opción seleccionada?",
        {
            title:"Alerta",
            buttons:{
                close:{
                    className:"deep-orange lighten-1",
                    text:"No",
                },
                confirm:{
                    className:"deep-orange lighten-1",
                    text:"Si",
                    callback:function(){
                        delete_option(objeto,id);
                    }
                }
            }
        }
    );
}

/**
 * Función para eliminar una pregunta
 * @param id Recibe el id de la pregunta
**/
function del_pregunta(id) {
    MaterialDialog.dialog(
        "¿Desea borrar la pregunta seleccionada?",
        {
            title:"Alerta",
            buttons:{
                close:{
                    className:"deep-orange lighten-1",
                    text:"No",
                },
                confirm:{
                    className:"deep-orange lighten-1",
                    text:"Si",
                    callback:function(){
                        delete_question(id);
                    }
                }
            }
        }
    );
}

/**
 * Función para abrir el formulario de preguntas
 * @param id Recibe el id de la consulta
**/
function add_preguntas(id) {
    var token = $('input').val();
    var html = '<form action="" role="form" method="post" id="question_form">';
    html += '<input type="hidden" name="csrfmiddlewaretoken" value="'+token+'">';
    html += '<div class="content">'
    html += '<a class="deep-orange-text lighten-1" href="#" onclick="agregar_preguntas(\'#preguntas_base\');">';
    html += '<i class="tiny material-icons">add_circle_outline</i> Agregar Preguntas</a></div>';
    html += '<div id="agregar_preguntas">';
    html += $('#preguntas_base').html();
    html += '</div></form>';
    MaterialDialog.dialog(
        html,
        {
            title:"Agregar Preguntas",
            buttons:{
                // Use by default close and confirm buttons
                close:{
                    className:"deep-orange lighten-1",
                    text:"Cerrar",
                },
                confirm:{
                    className:"deep-orange lighten-1",
                    text:"Guardar",
                    callback:function(){
                        validate_question(id);
                    }
                }
            }
        }
    );
    $('select').material_select();
}

/**
 * Función para abrir el formulario de preguntas
 * @param id Recibe el id de la consulta
**/
function validate_question(id) {
    var vacio = false;
    $.each($('.material-dialog').last().find('.modal-content #id_texto_pregunta'),function(key,value){
        if ($(value).val().trim()=='') {
            vacio = true;
        }
    });
    $.each($('.material-dialog').last().find('.modal-content #id_tipo_pregunta'),function(key,value){
        if ($(value).val().trim()=='') {
            vacio = true;
        }
    });
    if (vacio) {
        M.toast({html:"Debe llenar todas las preguntas que agregó"});
    }
    else{
        create_question(id);
    }
}

/**
 * Función para crear un pregunta
 * @param id Recibe el id de la consulta
**/
function create_question(id) {
    var form = $("#question_form");
    $.ajax({
    type: 'POST',
    data: $(form).serialize(),
    url: URL_CREAR_PREGUNTAS+id,
    success: function(response) {
        if (response.code) {
            M.toast({html:"Se crearon/creó la(s) pregunta(s) con éxito"});
        }
        else{
            var errors = '';
            $.each(response.errors,function(key,value){
                errors += key+" "+value+"<br>";
            });
            M.toast({html:errors});
        }
    },
        error:function(error)
        {
            M.toast({html:"Ocurrió un error inesperado"});
        }
    });
}

/**
 * Función para eliminar un pregunta
 * @param id Recibe el id de la pregunta
**/
function delete_question(id) {
    var token = $('input').val();
    var input = '';
    $.each($('#question_form').find('input'),function(index,value){
        if ($(value).attr('name') == 'texto_pregunta_id' && $(value).val() == id) {
            input = value;
        }
    });
    $.ajax({
        data: {'csrfmiddlewaretoken':token},
        type: 'POST',
        url: URL_ELIMINAR_PREGUNTAS+id,
        success: function(response) {
            if (response.success) {
                $(input).parent().parent().parent().parent().remove();
                M.toast({html:"Se eliminó la pregunta con éxito"});
            }
            else {
                M.toast({html:response.mensaje});
            }
        },
        error:function(error)
        {
            M.toast({html:"Ocurrió un error inesperado"});
        }
    }); 
}

/**
 * Función para eliminar un opcion
 * @param id Recibe el id de la opcion
**/
function delete_option(objeto,id) {
    var token = $('input').val();
    var input = '';
    $.each($(objeto).find('#option_form input'),function(index,value){
        if ($(value).attr('name') == 'texto_opcion_id' && $(value).val() == id) {
            input = value;
        }
    });
    $.ajax({
        data: {'csrfmiddlewaretoken':token},
        type: 'POST',
        url: URL_ELIMINAR_OPCIONES+id,
        success: function(response) {
            if (response.success) {
                $(objeto).parent().parent().remove();
                M.toast({html:"Se eliminó la opción con éxito"});
            }
            else {
                M.toast({html:response.mensaje});
            }
        },
        error:function(error)
        {
            M.toast({html:"Ocurrió un error inesperado"});
        }
    }); 
}
/**
 * Función para actualizar las preguntas de una consulta
**/
function update_question() {
    var form = $("#question_form");
    $.ajax({
        data: $(form).serialize(), 
        type: 'POST',
        url: URL_ACTUALIZAR_PREGUNTAS,
        success: function(response) {
            if (response.code) {
                M.toast({html:"Se actualizaron las preguntas con éxito"});
            }
            else{
                var errors = '';
                $.each(response.errors,function(key,value){
                    errors += key+" "+value+"<br>";
                });
                M.toast({html:errors});
            }
        },
        error:function(error)
        {
            M.toast({html:"Ocurrió un error inesperado"});
        }
    }); 
}


/**
 * @brief Función que actualiza los datos de combos dependientes
 * @param opcion Código del elemento seleccionado por el cual se filtrarán los datos en el combo dependiente
 * @param app Nombre de la aplicación en la cual buscar la información a filtrar
 * @param mod Modelo del cual se van a extraer los datos filtrados según la selección
 * @param campo Nombre del campo con el cual realizar el filtro de los datos
 * @param n_value Nombre del campo que contendra el valor de cada opción en el combo
 * @param n_text Nombre del campo que contendrá el texto en cada opción del combo
 * @param combo_destino Identificador del combo en el cual se van a mostrar los datos filtrados
 * @param bd Nombre de la base de datos, si no se específica se asigna el valor por defecto
 */
function actualizar_combo(opcion, app, mod, campo, n_value, n_text, combo_destino, bd) {
    /* Verifica si el parámetro esta definido, en caso contrario establece el valor por defecto */
    bd = typeof bd !== 'undefined' ? bd : 'default';
    $.ajaxSetup({
        async: false
    });
    $.getJSON(URL_ACTUALIZAR_COMBO, {
        opcion:opcion, app:app, mod:mod, campo:campo, n_value:n_value, n_text: n_text, bd:bd
    }, function(datos) {

        var combo = $("#"+combo_destino);

        if (datos.resultado) {

            if (datos.combo_disabled == "false") {
                combo.removeAttr("disabled");
            }
            else {
                combo.attr("disabled", "true");
            }

            combo.html(datos.combo_html);
        }
        else {
            bootbox.alert(datos.error);
            console.log(datos.error);
        }
    }).fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        bootbox.alert( 'Petición fállida' + err );
        console.log('Petición fállida ' + err)
    });
}

/**
 * @brief Función para recargar el captcha vía json
 * @param element Recibe el botón
 */
function refresh_captcha(element) {
    $form = $(element).parents('form');
    var url = location.protocol + "//" + window.location.hostname + ":" + location.port + "/captcha/refresh/";

    $.getJSON(url, {}, function(json) {
        $form.find('input[name="captcha_0"]').val(json.key);
        $form.find('img.captcha').attr('src', json.image_url);
    });

    return false;
}

/**
 * Función para mostrar el modal de confimación para generar el token
 * @param id Recibe el id de la consulta
**/
function modal_token(id) {
    var form = $('#formulario').html();
    var html = '<h4>¿Desea generar un nuevo token?</h4>';
    html += "<p>Su token será sobreescrito, y ya no podra consumir por servicios rest por el antiguo. <br>";
    html += "Recuerde cambiar el token en su otra aplicación.</p>";
    form = form.replace('/>','/>'+html);
    MaterialDialog.dialog(
        form,
        {
            title:"Alerta",
            buttons:{
                close:{
                    className:"deep-orange lighten-1",
                    text:"No",
                },
                confirm:{
                    className:"deep-orange lighten-1",
                    text:"Si",
                    callback:function(){
                        generate_token(id);
                    }
                }
            }
        }
    );
}

/**
 * Función para  generar el token
 * @param id Recibe el id de la consulta
**/
function generate_token(id){
    var form = $("#formulario_modal");
    $.ajax({
        data: $(form).serialize(), 
        type: 'POST',
        url: URL_GENERAR_TOKEN+id,
        success: function(response) {
            if (response.code) {
                M.toast({html:"Se actualizó el token con éxito"});
                setTimeout(function(){
                    location.reload();    
                },2000);
            }
            else{
                var errors = '';
                $.each(response.errors,function(key,value){
                    errors += key+" "+value+"<br>";
                });
                M.toast({html:errors});
            }
        },
        error:function(error)
        {
            M.toast({html:"Ocurrió un error inesperado"});
        }
    }); 
}
