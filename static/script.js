async function fetchResults(query) {
    const response = await fetch(`/?query=${encodeURIComponent(query)}&json=1`);
    return await response.json();
}

function renderResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    data.results.forEach(res => {
        const poster = res.poster_path
            ? `https://image.tmdb.org/t/p/w200${res.poster_path}`
            : "https://placehold.co/200x300?text=No%20Poster";

        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <img src="${poster}">
            <div class="card-content">
                <span class="type-label">${res.search_type.toUpperCase()}</span>
                <h2>${res.name}</h2>
                <p><strong>ID:</strong> ${res.id}</p>
                <p><strong>Release:</strong> ${res.release_date}</p>
                <p>${res.overview.slice(0, 100)}...</p>
            </div>
        `;

        card.onclick = () => {
            window.location.href = `/?play=${res.id}&type=${res.search_type}`;
        };

        container.appendChild(card);
    });
}

document.getElementById("searchBtn").addEventListener("click", async () => {
    const query = document.getElementById("searchInput").value;
    if (!query) return;
    const data = await fetchResults(query);
    renderResults(data);
});
