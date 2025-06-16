
const verifyBtn = document.getElementById('verify-btn');
const cuitInput = document.getElementById('cuit');
const jurSelect = document.getElementById('jurisdiccion');
const resultCard = document.getElementById('result-card');
const resultMessage = document.getElementById('result-message');
const resultTitle = document.getElementById('result-title');

verifyBtn.addEventListener('click', async () => {
    const cuit = cuitInput.value.trim();
    const jur = jurSelect.value;

    if (cuit.length !== 11 || !/^\d+$/.test(cuit)) {
        alert('Por favor, ingresá un CUIT válido de 11 dígitos numéricos.');
        return;
    }

    // Mostrar estado de carga
    resultTitle.textContent = 'Verificando...';
    resultMessage.textContent = 'Consultando los padrones en tiempo real. Por favor, esperá.';
    resultCard.classList.remove('hidden');
    verifyBtn.disabled = true;
    verifyBtn.textContent = 'Consultando...';

    try {
        const response = await fetch(`/api/verify?cuit=<span class="math-inline">\{cuit\}&jur\=</span>{jur}`);
        const data = await response.json();

        resultTitle.textContent = 'Resultado';

        if (data.error) {
            resultMessage.textContent = `Error: ${data.error}`;
        } else if (data.encontrado) {
            resultMessage.innerHTML = 
                `El CUIT <strong>${data.cuit_consultado}</strong> <span class="cuit-found">SÍ</span> se encuentra en el padrón de ${data.jurisdiccion}.<br><br>` +
                `<strong>${data.resultado.mensaje}</strong><br><br>` +
                `<small>Fuente: ${data.fuente_de_datos.nombre_padron}</small>`;
        } else {
            resultMessage.innerHTML = 
                `El CUIT <strong>${data.cuit_consultado}</strong> <span class="cuit-not-found">NO</span> se encuentra en el padrón de ${data.jurisdiccion}.<br><br>` +
                `No corresponde aplicar retención según la información disponible.<br><br>` +
                `<small>Fuente: ${data.fuente_de_datos.nombre_padron}</small>`;
        }

    } catch (error) {
        resultTitle.textContent = 'Error de Conexión';
        resultMessage.textContent = 'No se pudo comunicar con el servidor. Por favor, intentá de nuevo más tarde.';
    } finally {
        // Reactivar el botón
        verifyBtn.disabled = false;
        verifyBtn.textContent = 'Verificar CUIT';
    }
});
