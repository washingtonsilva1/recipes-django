var isExpanded = String(document.getElementById('acc-management').getAttribute('aria-expanded')).toString().toLowerCase() === 'true';

window.onload = function(ev) {
    document.getElementById('acc-management').addEventListener('click', function(ev) {
        ev.preventDefault();
        isExpanded = !isExpanded;
        document.getElementById('acc-management').setAttribute('aria-expanded', isExpanded);
    });
    document.querySelectorAll('.delete_recipe_form').forEach(function(e) {
        e.addEventListener('submit', function(ev) {
            ev.preventDefault();
            let delete_recipe = confirm('Are you sure?')
            if(delete_recipe) {
                e.submit();
            }
        });
    })
    document.querySelector('a.user-management-logout').addEventListener('click', function(ev) {
        ev.preventDefault()
        form = document.getElementById('user-management-logout')
        form.submit()
    })
}