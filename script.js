// --- NOTA IMPORTANTE: Lógica de Prototipo ---
// En esta versión, la verificación se hace contra una lista de CUITs de ejemplo
// para probar la interfaz. La versión real usará el motor de Python que te mostré.
const padronAGIP = {
    '20111111111': { alicuota: '3.00%' },
    '20222222222': { alicuota: '5.00%' }
};
const padronARBA = {
    '20333333333': { alicuota: '2.50%' },
    '20444444444': { alicuota: '4.00%' }
};

const verifyBtn = document.getElementById('verify-btn');
const cuitInput = document.getElementById('cuit');
const jurSelect = document.getElementById('jurisdiccion');
const resultCard = document.getElementById('result-card');
const resultMessage = document.getElementById('result-message');

verifyBtn.addEventListener('click', () => {
    const cuit = cuitInput.value.trim();
    const jur = jurSelect.value;

    if (cuit.length !== 11 || !/^\d+$/.test(cuit)) {
        alert('Por favor, ingresá un CUIT válido de 11 dígitos numéricos.');
        return;
    }

    let padron;
    if (jur === 'AGIP') {
        padron = padronAGIP;
    } else {
        padron = padronARBA;
    }

    const data = padron[cuit];

    if (data) {
        resultMessage.innerHTML = `El CUIT <span class="cuit-found">${cuit}</span> <span class="cuit-found">SÍ</span> se encuentra en el padrón de <span class="math-inline">\{jur\}\.<br\>Alícuota de Retención\: <strong\></span>{data.alicuota}</strong>.`;
    } else {
        resultMessage.innerHTML = `El CUIT <span class="cuit-not-found">${cuit}</span> <span class="cuit-not-found">NO</span> se encuentra en el padrón de ${jur}. No corresponde aplicar retención.`;
    }

    resultCard.classList.remove('hidden');
});
