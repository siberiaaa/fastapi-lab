function delete_categoria(id) {
    fetch('/categorias/' + id, {method:'DELETE'})
    .then(location.reload(true));
}

function delete_tipo_producto(id) {
    fetch('/tipos_productos/' + id, {method:'DELETE'})
    .then(location.reload(true));
}


function mostrar_imagen() {
    var input = document.getElementById("extraccion");
    var fReader = new FileReader();
    fReader.readAsDataURL(input.files[0]);
    fReader.onloadend = function(event) {
        var img = document.getElementById("imagen");
        img.value = event.target.result;
        img = document.getElementById('externa')
        img.src = event.target.result
        console.log(event.target.result);
        return event.target.result
    }
}

function deimaginar() {
    let imagen = document.getElementById('extraccion')
    let externa = document.getElementById('externa')
    let vistas = document.getElementById('imagen')
    imagen.value = ''
    externa.src = ''
    vistas.value = ''
}

function buscar_productos(data) {
    console.log(data);
    console.log(data.form);
    let resultado = data.value 
    data.form.submit()
}

function agregar_nueva_caracteristica() {
    console.log('holaaaaaaaaaaaaa');
    let nombre = document.getElementById('nombre')
    let descripcion = document.getElementById('descripcion')
    if (nombre.value == "" || descripcion.value == '') {
        return
    }
    let caracteristicas = document.getElementById('caracteristicas')
    let opcion = document.createElement('option')
    opcion.selected = true
    let nuevo = {
        'nombre': nombre.value, 
        'descripcion': descripcion.value
    }
    opcion.value = JSON.stringify(nuevo)
    opcion.innerText = nuevo.nombre
    opcion.setAttribute('ondblclick', 'borrar_uno(this);')
    console.log(opcion);
    nombre.value = ''
    descripcion.value = ''
    caracteristicas.appendChild(opcion)
}
function borrar_uno(data) {
    data.remove()
}