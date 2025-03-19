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
function modificarCantidad(id, accion, tipo) {
    if (!id || !tipo) {
        console.error("Error: ID o tipo de producto no definido", { id, tipo });
        return;
    }
    let cantidad = accion === "sumar" ? 1 : -1;
    let csrfToken = getCSRFToken();
    
    console.log(`Modificando cantidad: ID=${id}, Acción=${accion}, Tipo=${tipo}`);

    $.ajax({
        url: "/carrito/actualizar/",
        type: "POST",
        headers: { "X-CSRFToken": csrfToken },
        contentType: "application/json",
        data: JSON.stringify({ item_id: id, tipo: tipo, cantidad: cantidad }),
        success: function(response) {
            console.log("Cantidad actualizada correctamente:", response);
            let cantidadElemento = $(`.carrito-item[data-id="${id}"] .cantidad`);
            let nuevaCantidad = parseInt(cantidadElemento.text() || "0") + cantidad;
            if (nuevaCantidad <= 0) {
                $(`.carrito-item[data-id="${id}"]`).remove();
            } else {
                cantidadElemento.text(nuevaCantidad);
            }
        },
        error: function(xhr) {
            console.error("Error al modificar la cantidad:", xhr.responseText);
            alert("Error al modificar la cantidad del producto.");
        }
    });
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
            data: JSON.stringify({ item_id: id, tipo: tipo }),
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
        modificarCantidad(id, "sumar", tipo);
    });

    // Disminuir cantidad
    $(document).on("click", ".btn-restar", function(event) {
        event.preventDefault();
        let item = $(this).closest(".carrito-item");
        let id = item.data("id");
        let tipo = item.data("tipo");
        modificarCantidad(id, "restar", tipo);
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
            url: "/carrito/eliminar/",
            type: "POST",
            headers: { "X-CSRFToken": csrfToken },
            contentType: "application/json",
            data: JSON.stringify({ item_id: id, tipo: tipo }),
            success: function(response) {
                console.log("Producto eliminado correctamente:", response);
                $(`.carrito-item[data-id="${id}"]`).remove();
            },
            error: function(xhr) {
                console.error("Error al eliminar producto:", xhr.responseText);
                alert("Error al eliminar producto del carrito");
            }
        });
    });
});
