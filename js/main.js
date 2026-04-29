// AI Tool Finder - Main JS
document.addEventListener('DOMContentLoaded', function() {
  // Search functionality
  var searchInput = document.getElementById('tool-search');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      var query = this.value.toLowerCase();
      document.querySelectorAll('.tool-card').forEach(function(card) {
        var name = card.querySelector('.tool-name').textContent.toLowerCase();
        var desc = card.querySelector('.tool-desc').textContent.toLowerCase();
        card.style.display = (name.includes(query) || desc.includes(query)) ? '' : 'none';
      });
    });
  }
  
  // FAQ toggle
  document.querySelectorAll('.faq-question').forEach(function(q) {
    q.addEventListener('click', function() {
      this.parentElement.classList.toggle('open');
    });
  });
  
  // Category filter on compare page
  var filterSelect = document.getElementById('category-filter');
  if (filterSelect) {
    filterSelect.addEventListener('change', function() {
      var cat = this.value;
      document.querySelectorAll('.compare-row').forEach(function(row) {
        row.style.display = (!cat || row.dataset.category === cat) ? '' : 'none';
      });
    });
  }
});
