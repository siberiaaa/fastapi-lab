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