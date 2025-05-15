// Elementos del DOM
const btnNuevaCategoria = document.getElementById("btn-nueva-categoria");
const listaCategorias = document.getElementById("lista-categorias");
const inputCategoria = document.getElementById("categoria");
const formMonto = document.getElementById("form-monto");

// Función para crear un nuevo elemento de categoría
function crearCategoria(nombre) {
  const li = document.createElement("li");
  li.textContent = nombre;
  li.classList.add("categoria-item");

  // Agrega el evento de clic para seleccionar la categoría
  li.addEventListener("click", () => {
    inputCategoria.value = nombre;
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

// Evento de guardar monto máximo
formMonto.addEventListener("submit", (e) => {
  e.preventDefault();

  const categoria = inputCategoria.value;
  const monto = document.getElementById("monto-maximo").value;

  if (!categoria) {
    alert("Selecciona una categoría primero.");
    return;
  }

  if (!monto || isNaN(monto) || Number(monto) <= 0) {
    alert("Ingresa un monto válido.");
    return;
  }

  alert(`Monto máximo de $${monto} definido para "${categoria}".`);
  formMonto.reset();
});
