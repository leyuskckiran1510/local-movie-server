let currentQuery = '';

async function fetchResults(query) {
    const response = await fetch(`/?query=${encodeURIComponent(query)}&json=1`);
    return await response.json();
}

function formatRating(rating) {
    return rating ? rating.toFixed(1) : 'N/A';
}

function formatPopularity(popularity) {
    if (!popularity) return 'N/A';
    if (popularity >= 1000) return (popularity / 1000).toFixed(1) + 'K';
    return Math.round(popularity).toString();
}

function formatYear(dateString) {
    if (!dateString) return 'TBA';
    return dateString.split('-')[0];
}

function renderResults(data) {
    const container = document.getElementById("results");
    
    if (!data.results || data.results.length === 0) {
        container.innerHTML = '<div class="no-results">No results found. Try a different search.</div>';
        return;
    }

    container.innerHTML = "";

    data.results
        .sort((a, b) => (b.popularity || 0) - (a.popularity || 0))
        .forEach(res => {
            const poster = res.poster_path
                ? `https://image.tmdb.org/t/p/w300${res.poster_path}`
                : "https://placehold.co/300x450/2f2f2f/666?text=No+Poster";

            const card = document.createElement("div");
            card.className = "card";
            
            const rating = formatRating(res.vote_average);
            const year = formatYear(res.release_date);
            const popularity = formatPopularity(res.popularity);
            const overview = res.overview ? res.overview.slice(0, 150) : 'No overview available.';

            card.innerHTML = `
                <img src="${poster}" alt="${res.name}" loading="lazy">
                <div class="card-overlay"></div>
                <div class="play-icon"></div>
                <span class="type-label">${res.search_type.toUpperCase()}</span>
                <div class="card-content">
                    <h2>${res.name}</h2>
                    <div class="card-meta">
                        <div class="rating">
                            <span class="rating-star">★</span>
                            <span>${rating}</span>
                        </div>
                        <span class="year">${year}</span>
                        <div class="popularity" title="Popularity score">
                            <span>🔥</span>
                            <span>${popularity}</span>
                        </div>
                    </div>
                    <p>${overview}</p>
                </div>
            `;

            card.onclick = () => {
                window.location.href = `/?play=${res.id}&type=${res.search_type}`;
            };

            container.appendChild(card);
        });
}

async function performSearch() {
    const query = document.getElementById("searchInput").value.trim();
    if (!query) return;
    
    if (query === currentQuery) return;
    currentQuery = query;

    const container = document.getElementById("results");
    container.innerHTML = '<div class="loading">Searching...</div>';

    try {
        const data = await fetchResults(query);
        renderResults(data);
    } catch (error) {
        container.innerHTML = '<div class="no-results">Error loading results. Please try again.</div>';
        console.error('Search error:', error);
    }
}

document.getElementById("searchBtn").addEventListener("click", performSearch);

document.getElementById("searchInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        performSearch();
    }
});

let scrollTimeout;
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    clearTimeout(scrollTimeout);
    
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

document.getElementById("searchInput").focus();