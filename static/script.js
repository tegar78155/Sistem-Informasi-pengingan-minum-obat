// static/script.js
function toggleStatus(id) {
    fetch(`/update_status/${id}`, { method: 'POST' })
        .then(res => res.json())
        .then(() => window.location.reload());
}
