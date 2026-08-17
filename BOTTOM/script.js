const formulario = document.getElementById('miFormulario');
const btnCancelar = document.getElementById('btnCancelar');
const mensaje = document.getElementById('mensaje');

// Procesar el envío del formulario
formulario.addEventListener('submit', (event) => {
  event.preventDefault(); // Evita que la página se recargue
  
  const nombre = document.getElementById('nombre').value;
  mensaje.style.color = '#28a745';
  mensaje.textContent = `¡Datos guardados con éxito, ${nombre}!`;
});

// Acción del botón Cancelar
btnCancelar.addEventListener('click', () => {
  formulario.reset(); // Limpia todos los campos del formulario
  mensaje.style.color = '#dc3545';
  mensaje.textContent = 'Formulario cancelado y limpiado.';
});