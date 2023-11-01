var isExpanded = String(document.getElementById('acc-management').getAttribute('aria-expanded')).toString().toLowerCase() === 'true';

window.onload = function(e) {
    document.getElementById('acc-management').addEventListener('click', function(e) {
        isExpanded = !isExpanded;
        document.getElementById('acc-management').setAttribute('aria-expanded', isExpanded) 
    });
}