function delete_categoria(id){
    fetch('/categorias/'+id,{method:'DELETE'})
    .then(location.reload(true));
}