function delete_categoria(id) {
    fetch('/categorias/' + id, {method:'DELETE'})
    .then(location.reload(true));
}

function delete_tipo_producto(id) {
    fetch('/tipos_productos/' + id, {method:'DELETE'})
    .then(location.reload(true));
}

function consultar_producto(id){
    fetch('/productos/'+id,{method:'GET'})
    .then(location.reload(true));
}