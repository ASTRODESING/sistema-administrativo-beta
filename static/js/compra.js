function calculo_dinero_restante() {
    const presupuesto = document.getElementById("presupuesto")
    const subtotales = document.getElementsByClassName("subtotales")
    var total_subtotales = 0


    for (let i = 0; i < subtotales.length; i++) {
        total_subtotales += parseFloat(subtotales[i].textContent)
        var total = parseFloat(presupuesto.value) - total_subtotales
        var total_formateado = total.toFixed(2)
        dinero_restante.value = total_formateado

        console.log(total)
    }

    if (parseInt(dinero_restante.innerHTML) < 0) {
        dinero_restante.className = "negativo"
    } else {
        dinero_restante.className = ""
    }
}


function btn_añadir(evt) {
    evt.preventDefault()

    var row = document.createElement("tr");
    var celda_nombre = document.createElement("th");
    var celda_precio = document.createElement("th");
    var celda_cantidad = document.createElement("th");
    var celda_subtotal = document.createElement("th");
    var celda_eliminar = document.createElement("th");

    var cantidad = document.createElement("input");

    cantidad.name = `stock`
    cantidad.className = `cantidad`
    cantidad.placeholder = 'Ingrese Cantidad Producto'
    cantidad.type = 'number'
    cantidad.value = 1
    cantidad.name = "cantidad"
    celda_cantidad.appendChild(cantidad)

    var precio = document.createElement("input");
    precio.name = `precio`
    precio.className = `precio`
    precio.placeholder = 'Ingrese Precio Producto'
    precio.type = 'number'
    precio.value = 1
    precio.name = "precio"
    celda_precio.appendChild(precio)

    var nombre = document.createElement("input");
    nombre.name = `producto`
    nombre.className = `nombre`
    nombre.type = 'text'
    nombre.value = ``
    nombre.name = "nombre_producto"
    celda_nombre.appendChild(nombre)

    var btn_eliminar = document.createElement("button")
    btn_eliminar.textContent = 'X'
    btn_eliminar.className = 'btn_eliminar'
    btn_eliminar.id = 'btn_eliminar'
    btn_eliminar.onclick = function (event) {
        event.preventDefault()

        const btn_eliminar = document.getElementById('btn_eliminar')
        const fila = btn_eliminar.parentNode.parentNode
        fila.remove()

    }
    celda_eliminar.appendChild(btn_eliminar)
    celda_subtotal.className = `subtotales`
    celda_subtotal.innerText = 1

    row.appendChild(celda_nombre)
    row.appendChild(celda_precio)
    row.appendChild(celda_cantidad)
    row.appendChild(celda_subtotal)
    row.appendChild(celda_eliminar)
    tabla_productos.appendChild(row)

}



function calculo(event) {
    event.preventDefault()
    var precio = document.getElementsByClassName("precio")
    var cantidad = document.getElementsByClassName("cantidad")
    var subtotal_sin_formato = 0


    for (let i = 0; i < cantidad.length; i++) {
        subtotal_sin_formato = parseFloat(cantidad[i].value) * parseFloat(precio[i].value)
        var subtotal_formateado = subtotal_sin_formato.toFixed(2)
        cantidad[i].parentNode.nextElementSibling.innerHTML = subtotal_formateado



    }
    calculo_dinero_restante()

}

$(document).ready(function () {
    $('#buscador_proveedor').select2();
});