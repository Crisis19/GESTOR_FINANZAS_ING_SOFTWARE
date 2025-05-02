function actualizarProgreso() {
  const monto = parseFloat(document.getElementById("monto").value) || 0;
  const ahorro = parseFloat(document.getElementById("ahorro").value) || 0;
  const abono = parseFloat(document.getElementById("abono").value) || 0;

  const totalAhorro = ahorro + abono;
  const progreso = monto > 0 ? Math.min((totalAhorro / monto) * 100, 100) : 0;

  const barra = document.getElementById("progreso");
  barra.style.width = progreso + "%";
  barra.textContent = progreso.toFixed(1) + "%";
}

document.addEventListener("DOMContentLoaded", () => {
  const formulario = document.getElementById("meta-form");
  
  formulario.addEventListener("submit", (e) => {
    e.preventDefault(); // Prevenimos el envío del formulario para no recargar la página
    actualizarProgreso();
  });

  document.getElementById("monto").addEventListener("input", actualizarProgreso);
  document.getElementById("ahorro").addEventListener("input", actualizarProgreso);
  document.getElementById("abono").addEventListener("input", actualizarProgreso);
});
