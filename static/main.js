// main.js

const tbody = document.querySelector("#itemsTable tbody");
const searchInput = document.getElementById("search");
let data = []; // This will hold the full dataset fetched from the server

// --- Utility Functions ---

function formatCurrency(n) {
    // keep 2 decimals, local formatting
    return Number(n).toLocaleString(undefined, {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    });
}

function escapeHtml(str) {
    // simple HTML escaper (safe for this demo)
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function renderRows(rows) {
    if (rows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px;">No items match your search.</td></tr>';
        return;
    }
    tbody.innerHTML = rows
        .map(
            (r) => `
        <tr>
          
        <td id="item-sell" class="num">${formatCurrency(r.sell)}</td>
        <td id="item-cost" class="num">${formatCurrency(r.cost)}</td>
        <td id="item-name" style="text-align: right;" class="name-col">${escapeHtml(r.name)}</td>
        <td class="id-col">${r.barcode}</td>
        </tr>
      `
        )
        .join("");
}

// --- Data Fetching and Initial Render ---

async function fetchAndRenderData() {
    try {
        const response = await fetch('/api/items');
        data = await response.json();
        renderRows(data);
    } catch (error) {
        console.error("Error fetching data:", error);
        tbody.innerHTML = '<tr><td colspan="4" style="color: red; text-align: center;">Failed to load item data.</td></tr>';
    }
}

fetchAndRenderData();


// --- Filtering/Search Support ---

searchInput.addEventListener("input", (e) => {
    const searchTerm = e.target.value.toLowerCase().trim();
    console.log("Search term:", searchTerm);
    if (!searchTerm) {
        // If the search box is empty, render the full dataset (data)
        renderRows(data);
        return;
    }
    // This is where the filtering happens:
    // It creates a NEW array (filteredItems) containing ONLY the matches.
    const filteredItems = data.filter((item) => {
        return (
            // Check name
            item.name.toLowerCase().includes(searchTerm) ||
            // Check barcode
            // item.barcode.includes(searchTerm) ||
            // Check ID (needs to be converted to string for includes)
            item.id.toString().includes(searchTerm)
        );
    });

    // Only the filtered (matching) items are passed to the renderer.
    // Non-matching items are effectively "display: none" because they are never added to the DOM.
    renderRows(filteredItems);
    
});


// --- Sorting Support ---

let sortState = { key: null, dir: 1 }; // dir: 1 asc, -1 desc

document.querySelectorAll("#itemsTable thead th").forEach((th) => {
    th.addEventListener("click", () => {
        const key = th.dataset.key;
        
        // toggle sort direction
        if (sortState.key === key) sortState.dir *= -1;
        else {
            sortState.key = key;
            sortState.dir = 1; // Default to ascending when changing column
        }

        // remove sort markers from all headers
        document
            .querySelectorAll("#itemsTable thead th")
            .forEach((h) => h.classList.remove("sort-asc", "sort-desc"));

        // add current sort marker
        if (sortState.dir === 1) th.classList.add("sort-asc");
        else th.classList.add("sort-desc");

        // Get the currently displayed data (either full or filtered)
        // We look at the data currently being displayed in the table
        const currentDataToFilter = searchInput.value.trim() ? data.filter((item) => {
             // Re-run the filter logic for sorting the correct subset
             const searchTerm = searchInput.value.toLowerCase().trim();
             return (
                item.name.toLowerCase().includes(searchTerm) ||
                item.barcode.includes(searchTerm) ||
                item.id.toString().includes(searchTerm)
            );
        }) : data;


        const sorted = currentDataToFilter.slice().sort((a, b) => {
            let av = a[key],
                bv = b[key];
            
            // Numeric comparison for id, cost, and sell
            if (['id', 'cost', 'sell'].includes(key)) 
                return (Number(av) - Number(bv)) * sortState.dir;
            
            // String comparison fallback for name/barcode
            return av.toString().localeCompare(bv.toString()) * sortState.dir;
        });

        renderRows(sorted);
    });
});