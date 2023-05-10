function CalculoDineroRestante() {
    const presupuesto = document.getElementById("presupuesto")
    const dinero_restante = document.getElementById("dinero_restante")
    const subtotales = document.getElementsByClassName("subtotales")
    var total =0






    presupuesto.addEventListener("keydown", function () {

        for(let i = 0; i < subtotales.length; i++){
            total += parseFloat(subtotales[i].textContent)
            var total_formateado = total.toFixed(2)
            dinero_restante.innerText = presupuesto - total_formateado
        }


    })
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
    celda_cantidad.appendChild(cantidad)

    var precio = document.createElement("input");
    precio.name = `precio`
    precio.className = `cantidad`
    precio.placeholder = 'Ingrese Precio Producto'
    precio.type = 'number'
    precio.value = 1
    celda_precio.appendChild(precio)

    var nombre = document.createElement("input");
    nombre.name = `producto`
    nombre.className = `cantidad`
    nombre.type = 'text'
    nombre.value = ``
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
    celda_subtotal.className = `subtotal`

    row.appendChild(celda_nombre)
    row.appendChild(celda_precio)
    row.appendChild(celda_cantidad)
    row.appendChild(celda_subtotal)
    row.appendChild(celda_eliminar)
    tabla_productos.appendChild(row)

}




$(document).ready(function () {
    $('#buscador_proveedor').select2();
    calculo_dinero_restante();
    calculo_subtotales()
});

