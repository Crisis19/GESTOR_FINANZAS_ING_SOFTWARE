// Elementos del DOM
const btnNuevaCategoria = document.getElementById("btn-nueva-categoria");
const listaCategorias = document.getElementById("lista-categorias");
const inputCategoria = document.getElementById("categoria");
const inputMonto = document.getElementById("monto-maximo");
const formMonto = document.getElementById("form-monto");
var categorias = {};

// Función para crear un nuevo elemento de categoría
function crearCategoria(nombre) {
  fetch("/crear_categoria/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ nombre: nombre }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al crear la categoría");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Categoría creada:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("No se pudo crear la categoría.");
    });
  const li = document.createElement("li");
  li.textContent = nombre;
  li.classList.add("categoria-item");

  // Agrega el evento de clic para seleccionar la categoría
  li.addEventListener("click", () => {
    inputCategoria.value = nombre;
    inputMonto.value = ""; // Limpiar el campo de monto al seleccionar una categoría
  });

  listaCategorias.appendChild(li);
}

// Evento para añadir una nueva categoría
btnNuevaCategoria.addEventListener("click", () => {
  const nombre = prompt("Ingrese el nombre de la nueva categoría:");
  if (nombre && nombre.trim() !== "") {
    // Verificar que no esté repetida
    const yaExiste = Array.from(listaCategorias.children).some(
      (li) => li.textContent.toLowerCase() === nombre.trim().toLowerCase()
    );
    if (yaExiste) {
      alert("Esa categoría ya existe.");
      return;
    }

    crearCategoria(nombre.trim());
  }
});

// Delegación de eventos para los elementos <li>
listaCategorias.addEventListener("click", (event) => {
  // Verifica si el clic ocurrió en un elemento <li>
  if (event.target && event.target.tagName === "LI") {
    const nombre = event.target.textContent; // Obtén el texto del <li> clickeado
    inputCategoria.value = nombre; // Asigna el valor al input
    inputMonto.value = ""; // Limpiar el campo de monto al seleccionar una categoría
  }
});

