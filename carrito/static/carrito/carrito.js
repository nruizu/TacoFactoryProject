$(document).ready(function() {
    $(".btn-mas, .btn-menos, .btn-eliminar").click(function() {
        let item = $(this).closest(".carrito-item");
        let id = item.data("id");
        let tipo = item.data("tipo");
        let cantidad = $(this).hasClass("btn-mas") ? 1 : $(this).hasClass("btn-menos") ? -1 : 0;
        let url = cantidad ? `/carrito/actualizar/${tipo}/${id}/` : `/carrito/eliminar/${tipo}/${id}/`;

        $.post(url, { cantidad: cantidad, csrfmiddlewaretoken: "{{ csrf_token }}" }, function() {
            location.reload();
        });
    });
});
