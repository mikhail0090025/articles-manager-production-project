// search2.js
const { useState } = React;

function SearchArticles() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8004/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) throw new Error(response.statusText);

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setError("Error fetching results. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <div>
      <h1>Search Articles</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Enter search term"
      />
      <button onClick={handleSearch}>Search</button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <div>
        {results.length > 0 ? (
          results.map((article, index) => (
            <div key={index} className="result-item">
              <h3>{article.title}</h3>
              <p>{article.content}</p>
            </div>
          ))
        ) : (
          !loading && <p>No results found.</p>
        )}
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("search_results"));
root.render(React.createElement(SearchArticles));

document.getElementById("logout_button").addEventListener("click", () => {
    fetch("/logout", { method: "POST", credentials: "include" }).then(response => {
        if (response.ok) {
            console.log("Logout");
            window.location.assign("/login_page");
        } else {
            console.error("Logout failed:", response.statusText);
            window.location.assign("/login_page");
        }
    }).catch(error => {
        console.error("Logout error:", error);
        alert("An error occurred while logging out. Please try again.");
    });
});