$(document).ready(function() {
    function getCSRFToken() {
        return document.querySelector("input[name=csrfmiddlewaretoken]").value;
    }

    // Depuración para verificar si los botones tienen los atributos correctos
    $(".btn-agregar-carrito").each(function() {
        console.log("Verificando botón:", $(this).data());
    });

    // Agregar producto al carrito
    $(document).on("click", ".btn-agregar-carrito", function(event) {
        event.preventDefault();

        let idPlato = $(this).data("idplato");
        let idBebida = $(this).data("idbebida");
        let tipo = $(this).data("tipo");

        let id = idPlato || idBebida; // Soporte para ambos modelos

        console.log("Botón presionado - Datos obtenidos:", { idPlato, idBebida, tipo, id });

        if (!id || !tipo) {
            console.error("Error: ID o tipo de producto no definido en el botón.", $(this).data());
            return;
        }

        $.post("/carrito/agregar/", {
            item_id: id,
            tipo: tipo,
            csrfmiddlewaretoken: getCSRFToken()
        }).done(function(response) {
            alert("Producto agregado al carrito");
        }).fail(function(xhr) {
            console.error("Error al agregar producto:", xhr.responseText);
            alert("Error al agregar producto al carrito");
        });
    });

    // Actualizar o eliminar producto del carrito
    $(document).on("click", ".btn-mas, .btn-menos, .btn-eliminar", function(event) {
        event.preventDefault();

        let item = $(this).closest(".carrito-item");
        let id = item.data("id");
        let tipo = item.data("tipo");
        let cantidad = $(this).hasClass("btn-mas") ? 1 : $(this).hasClass("btn-menos") ? -1 : 0;
        let url = cantidad ? "/carrito/actualizar/" : "/carrito/eliminar/";

        console.log("Acción sobre carrito:", { id, tipo, cantidad });

        if (!id || !tipo) {
            console.error("Error: ID o tipo no definido en el item.", item.data());
            return;
        }

        $.post(url, {
            item_id: id,
            tipo: tipo,
            cantidad: cantidad,
            csrfmiddlewaretoken: getCSRFToken()
        }).done(function(response) {
            if (response.redirect) {
                window.location.href = response.redirect;
            } else {
                location.reload();
            }
        }).fail(function(xhr) {
            console.error("Error en la operación del carrito:", xhr.responseText);
            alert("Error en la operación del carrito");
        });
    });
});
