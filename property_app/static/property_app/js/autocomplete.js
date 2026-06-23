document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('autocomplete-results');

    if (!searchInput || !resultsContainer) return;

    searchInput.addEventListener('input', async function () {

        // Get the text the user typed, and trim off any accidental empty spaces at the beginning or end
        const value = this.value.trim();

        // If the user has typed less than 2 letters, hide the dropdown box and don't do anything yet
        if (value.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }

        try {
            // Ask  API to search for whatever the user typed
            const response = await fetch(`/api/v1/autocomplete/?q=${encodeURIComponent(value)}`);

            // Turn the raw answer from the backend into a clean list of data we can read
            const data = await response.json();

            // If the database didn't find any matching cities or countries, hide the dropdown box and stop
            if (data.length === 0) {
                resultsContainer.style.display = 'none';
                return;
            }

            // Loop through each matching place we found and create HTML links for them 
            resultsContainer.innerHTML = data.map(item => `
                <a href="${item.url}" class="list-group-item list-group-item-action py-2 d-flex justify-content-between align-items-center">
                    <div>
                        <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                        <strong>${item.display_text}</strong>
                    </div>
                    <span class="text-muted small">${item.subtitle}</span>
                </a>
            `).join('');

            resultsContainer.style.display = 'block';

        } catch (err) {
            // If the server crashes or the internet drops out, log the error in the browser console
            console.error('Error fetching filtered location assets:', err);
        }
    });

    // Listen for clicks anywhere on the entire screen
    document.addEventListener('click', function (e) {
        // If the user clicks outside of the search input box AND outside the dropdown box, close the dropdown
        if (e.target !== searchInput && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
});