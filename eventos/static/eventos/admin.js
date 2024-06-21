document.addEventListener('DOMContentLoaded', function() {
    var competenciaIndividual = document.getElementById('id_competencia_individual');
    var maxIntegrantes = document.getElementById('id_max_integrantes').closest('.form-row');

    function toggleMaxIntegrantes() {
        if (competenciaIndividual.checked) {
            maxIntegrantes.style.display = 'none';
        } else {
            maxIntegrantes.style.display = '';
        }
    }

    // Initial check
    toggleMaxIntegrantes();

    // Add event listener
    competenciaIndividual.addEventListener('change', toggleMaxIntegrantes);
});
