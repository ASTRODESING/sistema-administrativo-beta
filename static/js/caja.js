$(document).ready(function () {
    $('.buscador-etiqueta').select2();
    $('.buscador-codigo').select2();

});



function anadirProductoEtiqueta() {

    var producto_seleccion = document.getElementById("buscador_etiqueta")
    var producto_seleccionado = producto_seleccion.value

    const listarProducto = async (producto_seleccionado) => {



        const response = await fetch(`./getproducto/${producto_seleccionado}`)
        const datos = await response.json();

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

        var nombre = document.createElement("input");
        nombre.name = `producto`
        nombre.className = `cantidad`
        nombre.type = 'text'
        nombre.value = `${datos.nombre}`
        celda_nombre.appendChild(nombre)

        celda_precio.textContent = datos.precio
        celda_subtotal.className = `subtotal`

        var btn_eliminar = document.createElement("button")
        btn_eliminar.textContent = 'X'
        btn_eliminar.id = 'btn_eliminar'
        btn_eliminar.className = 'btn_eliminar'
        btn_eliminar.onclick = function (event) {
            event.preventDefault()

            const btn_eliminar = document.getElementById('btn_eliminar')
            const fila = btn_eliminar.parentNode.parentNode
            fila.remove()

        }
        celda_eliminar.appendChild(btn_eliminar)

                
        if (datos.excento == true){
            var celda_excento = document.createElement("th")
            celda_excento.textContent = true
            celda_subtotal.textContent = cantidad.value * datos.precio
        }
        else{
            var celda_excento = document.createElement("th")
            celda_excento.textContent = false
            var iva = (cantidad.value * datos.precio) * 0.16
            var subtotal_sinformato = (cantidad.value * datos.precio) + iva
            celda_subtotal.textContent = subtotal_sinformato.toFixed(2)
        }

        row.appendChild(celda_nombre)
        row.appendChild(celda_precio)
        row.appendChild(celda_cantidad)
        row.appendChild(celda_subtotal)
        row.appendChild(celda_excento)
        row.appendChild(celda_eliminar)

        var tabla_productos = document.getElementById("tabla_productos")
        tabla_productos.appendChild(row)
        calculo()
    }
    listarProducto(producto_seleccionado)

}

function anadirProductoCodigo() {

    var producto_seleccion = document.getElementById("buscador_codigo")
    var producto_seleccionado = producto_seleccion.value

    const listarProducto = async (producto_seleccionado) => {



        const response = await fetch(`./getproducto/${producto_seleccionado}`)
        const datos = await response.json();

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

        var nombre = document.createElement("input");
        nombre.name = `producto`
        nombre.className = `cantidad`
        nombre.type = 'text'
        nombre.value = `${datos.nombre}`
        celda_nombre.appendChild(nombre)

        celda_precio.textContent = datos.precio
        celda_subtotal.className = `subtotal`


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

                
        if (datos.excento == true){
            var celda_excento = document.createElement("th")
            celda_excento.textContent = true
            celda_subtotal.textContent = cantidad.value * datos.precio
        }
        else{
            var celda_excento = document.createElement("th")
            celda_excento.textContent = false
            var iva = (cantidad.value * datos.precio) * 0.16
            var subtotal_sinformato = (cantidad.value * datos.precio) + iva
            celda_subtotal.textContent = subtotal_sinformato.toFixed(2)
        }

        row.appendChild(celda_nombre)
        row.appendChild(celda_precio)
        row.appendChild(celda_cantidad)
        row.appendChild(celda_subtotal)
        row.appendChild(celda_excento)
        row.appendChild(celda_eliminar)

        var tabla_productos = document.getElementById("tabla_productos")
        tabla_productos.appendChild(row)
        calculo()
    }
    listarProducto(producto_seleccionado)

}

function calculo() {
    var fila_productos = document.getElementById("tabla_productos");

    var inputs_cantidad = fila_productos.getElementsByClassName("cantidad");
    var contador = 0
    while (contador < inputs_cantidad.length) {

        var input_cantidad = inputs_cantidad[contador];

            input_cantidad.addEventListener("keyup", function () {
                if (this.parentNode.nextElementSibling.nextElementSibling.innerHTML == 'true'){
                    console.log('dio true aqui esta el innerhtml =')
                    console.log(this.parentNode.nextElementSibling.nextElementSibling.innerHTML)
                    var cantidad = parseFloat(this.value);

                    var precio = parseFloat(this.parentNode.previousElementSibling.innerHTML);

    
                    var subtotal = cantidad * precio;
                    var subtotal_formateado = subtotal.toFixed(2)
    
                    this.parentNode.nextElementSibling.innerHTML = subtotal_formateado;

                } else{
                    console.log('dio false aqui esta el innerhtml =')
                    console.log(this.parentNode.nextElementSibling.nextElementSibling.innerHTML)

                    var cantidad = parseFloat(this.value);

                    var precio = parseFloat(this.parentNode.previousElementSibling.innerHTML);
    
    
                    var subtotal = cantidad * precio;
                    var subtotal_iva = subtotal * 0.16
                    var subtotal_sinformato = subtotal + subtotal_iva
                    var subtotal_formateado = subtotal_sinformato.toFixed(2)


    
                    this.parentNode.nextElementSibling.innerHTML = subtotal_formateado;

                }


            });
        

        contador++
    }
}



function calculo_total(evt) {
    evt.preventDefault();
    var fila_productos = document.getElementById("tabla_productos");
    var subtotal = fila_productos.getElementsByClassName("subtotal");

    var total = 0

    for (let i = 0; i < subtotal.length; i++) {

            total += parseFloat(subtotal[i].textContent);
            total_formateado = total.toFixed(2)



    }
    document.getElementById('total').innerHTML = total_formateado
}

