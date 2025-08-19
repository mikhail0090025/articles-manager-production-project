document.getElementById("search_button").addEventListener("click", async () => {
    const query = document.getElementById("search_query").value;
    const resultDiv = document.getElementById("search_results");
    resultDiv.innerHTML = ""; // Clear previous results

    try {
        const response = await fetch(`http://localhost:8004/search`, {
            method: "POST",
            body: JSON.stringify({ query: query }),
            headers: {
                "Content-Type": "application/json"
            }
        });
        if (!response.ok) {
            console.log(`Error: ${response.statusText}`);
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("Search results:", data);
        
        if (data.results && data.results.length > 0) {
            data.results.forEach(result => {
                const resultItem = document.createElement("div");
                resultItem.className = "result-item";
                resultItem.innerHTML = `<h3>${result.title}</h3><p>${result.content}</p>`;
                resultDiv.appendChild(resultItem);
            });
        }
        else {
            resultDiv.innerHTML = "<p>No results found.</p>";
        }
    } catch (error) {
        console.error("Error fetching search results:", error);
        resultDiv.innerHTML = "<p>Error fetching results. Please try again later.</p>";
    }
});

document.getElementById("search_query").addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent form submission
        document.getElementById("search_button").click(); // Trigger search button click
    }
});