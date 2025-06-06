// Obtener el token CSRF desde las cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith('csrftoken=')) {
                cookieValue = cookie.substring('csrftoken='.length);
            }
        });
    }
    if (!cookieValue) console.error("Error: No se encontró el token CSRF en las cookies.");
    return cookieValue;
}

// Función para modificar cantidad de productos en el carrito
function modificarCantidad(id, accion, tipo, cantidadElemento) {
    if (!id || !tipo) {
        console.error("Error: ID o tipo de producto no definido", { id, tipo });
        return;
    }

    let csrfToken = getCSRFToken();
    let $cantidadElemento = $(cantidadElemento);
    let cantidadActual = parseInt($cantidadElemento.text().trim());

    if (isNaN(cantidadActual)) {
        console.error("Cantidad actual no es un número válido:", $cantidadElemento.text());
        cantidadActual = 1;
    }

    let nuevaCantidad = accion === "sumar" ? cantidadActual + 1 : cantidadActual - 1;

    console.log(`Enviando cantidad: ${nuevaCantidad} (accion=${accion})`);

    $.ajax({
        url: "/carrito/actualizar/",
        type: "POST",
        headers: { "X-CSRFToken": csrfToken },
        contentType: "application/json",
        data: JSON.stringify({ item_id: id, tipo: tipo, cantidad: nuevaCantidad }),
        success: function(response) {
            console.log("Cantidad actualizada correctamente:", response);
            if (response.eliminado) {
                $(`.carrito-item[data-id="${id}"]`).remove();
            } else {
                $cantidadElemento.text(response.nueva_cantidad);
            }
            actualizarSubtotal();
        },
        error: function(xhr) {
            console.error("Error al modificar la cantidad:", xhr.responseText);
            alert("Error al modificar la cantidad del producto.");
        }
    });
}

function actualizarSubtotal() {
    let subtotal = 0;
    $(".carrito-item").each(function () {
        let cantidad = parseInt($(this).find(".cantidad").text().trim());
        let precio = parseFloat($(this).data("precio"));


        if (!isNaN(cantidad) && !isNaN(precio)) {
            subtotal += cantidad * precio;
        }
    });
    $("#subtotal").text(`$${subtotal.toFixed(2)}`);
}


$(document).ready(function() {
    console.log("carrito.js cargado correctamente");

    // Agregar producto al carrito
    $(document).on("click", ".btn-agregar-carrito", function(event) {
        event.preventDefault();
        let id = $(this).data("idplato") || $(this).data("idbebida");
        let tipo = $(this).data("tipo");
        let csrfToken = getCSRFToken();
        
        if (!id || !tipo) {
            console.error("Error: ID o tipo no definido en botón agregar.", $(this).data());
            return;
        }
        if (!csrfToken) {
            alert("Error: No se pudo obtener el token CSRF.");
            return;
        }
        
        console.log("Agregando producto al carrito:", { id, tipo });
        
        $.ajax({
            url: "/carrito/agregar/",
            type: "POST",
            headers: { "X-CSRFToken": csrfToken },
            contentType: "application/json",
            data: JSON.stringify({ item_id: id, tipo: tipo, cantidad: 1 }),
            success: function(response) {
                console.log("Producto agregado:", response);
                alert("Producto agregado al carrito");
            },
            error: function(xhr) {
                console.error("Error al agregar producto:", xhr.responseText);
                alert("Error al agregar producto al carrito");
            }
        });
    });

    // Aumentar cantidad
    $(document).on("click", ".btn-sumar", function(event) {
        event.preventDefault();
        let item = $(this).closest(".carrito-item");
        let id = item.data("id");
        let tipo = item.data("tipo");
        let cantidadElemento = item.find(".cantidad");
        modificarCantidad(id, "sumar", tipo, cantidadElemento);
    });

    // Disminuir cantidad
    $(document).on("click", ".btn-restar", function(event) {
        event.preventDefault();
        let item = $(this).closest(".carrito-item");
        let id = item.data("id");
        let tipo = item.data("tipo");
        let cantidadElemento = item.find(".cantidad");
        modificarCantidad(id, "restar", tipo, cantidadElemento);
    });

    // Eliminar producto
    $(document).on("click", ".btn-eliminar", function(event) {
        event.preventDefault();
        let item = $(this).closest(".carrito-item");
        let id = item.data("id");
        let tipo = item.data("tipo");
        let csrfToken = getCSRFToken();
        
        if (!id || !tipo) {
            console.error("Error: ID o tipo no definido en el item.", item.data());
            return;
        }
        if (!csrfToken) {
            alert("Error: No se pudo obtener el token CSRF.");
            return;
        }
        
        console.log("Eliminando producto del carrito:", { id, tipo });
        
        $.ajax({
            url: `/carrito/eliminar/${tipo}/${id}/`,  // URL corregida con los datos en la ruta
            type: "POST",
            headers: { "X-CSRFToken": csrfToken },
            success: function(response) {
                console.log("Producto eliminado correctamente:", response);
                $(`.carrito-item[data-id="${id}"]`).remove();
                actualizarSubtotal();
            },
            error: function(xhr) {
                console.error("Error al eliminar producto:", xhr.responseText);
                alert("Error al eliminar producto del carrito");
            }
        });
    });
});
