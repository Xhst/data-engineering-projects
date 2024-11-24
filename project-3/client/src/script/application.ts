import axios from "axios";
import WebSocket from "ws";

import { PaperSearchDto, TableSearchDto, isPaperSearchDto, isTableSearchDto } from "./model_dto";

console.log(
    '🚀 Developed by %c 🌲 Xhst, Prox, Diggi 🌲',
    'color: green; font-weight: bold;'
);

let searchInput = document.getElementById("search") as HTMLInputElement;

type SearchType = "papers" | "tables";

let currentSearchType: SearchType = "papers";

document.getElementById("search-type-papers").addEventListener("click", () => switchSearchTypes("papers"));
document.getElementById("search-type-tables").addEventListener("click", () => switchSearchTypes("tables"));

function switchSearchTypes(type: SearchType) {
    currentSearchType = type;
    document.getElementById('search-result').classList.add("d-none");

    switch (type) {
        case "papers":
            (document.getElementById("search-type-papers") as HTMLInputElement).checked = true;
            (document.getElementById("search-type-tables") as HTMLInputElement).checked = false;
        
            advancedSearchToggle.classList.remove("d-none");
            advancedSearchContainer.classList.remove("d-none");

            break;
        case "tables":
            (document.getElementById("search-type-tables") as HTMLInputElement).checked = true;
            (document.getElementById("search-type-papers") as HTMLInputElement).checked = false;

            advancedSearchToggle.classList.add("d-none");
            advancedSearchContainer.classList.add("d-none");

            break;
    }
}

searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        let query = searchInput.value;

        sendQuery(query);
    }
});


/*******************  THEME  ************************/
type Theme = 'light' | 'dark';

let currentTheme: Theme = 'light';

document.getElementById('theme-toggle').addEventListener('click', changeTheme);

function changeTheme() {
    let themeStylesheet = document.getElementById('theme-stylesheet') as HTMLLinkElement;

    if (currentTheme === 'light') {
        themeStylesheet.setAttribute('href', '/assets/css/style2.css');
        localStorage.setItem('theme', '/assets/css/style2.css'); // Stores the user's preference
        currentTheme = 'dark';
    } else {
        themeStylesheet.setAttribute('href', '/assets/css/style.css');
        localStorage.setItem('theme', '/assets/css/style.css'); // Stores the user's preference
        currentTheme = 'light';
    }

    document.body.setAttribute('data-bs-theme', currentTheme);
}

/*******************   PAPER -> ADVANCED SEARCH   ************************/
let advancedSearchToggle = document.getElementById("advanced-search-btn");
let advancedSearchContainer = document.getElementById("advanced-search");

let advancedSearchQueriesNumber = 0;
let addFilterButton = document.getElementById("as-add-filter-button")

let filtersIds: Set<number> = new Set();

function addPaperFilter() {
    advancedSearchQueriesNumber++;

    filtersIds.add(advancedSearchQueriesNumber);

    let filterInputTemplate = `
        <div id="as-filter-container-${advancedSearchQueriesNumber}" class="input-group mb-3">
            <select class="form-select" id="as-operator-${advancedSearchQueriesNumber}" style="max-width: 90px">
                <option value="and" selected>AND</option>
                <option value="or">OR</option>
                <option value="not">NOT</option>
            </select>
            <input id="as-query-${advancedSearchQueriesNumber}" type="text" class="form-control">
            <select id="as-filter-${advancedSearchQueriesNumber}" class="form-select" style="max-width: 120px">
                <option value="all" selected>All</option>
                <option value="title">Title</option>
                <option value="abstract">Abstract</option>
                <option value="keywords">Keywords</option>
                <option value="authors">Authors</option>
            </select>
            <button class="btn btn-outline-danger" id="as-remove-filter-${advancedSearchQueriesNumber}"><i class="bi bi-x"></i></button>
        </div>
        `;
    
    document.getElementById("as-filters-container").insertAdjacentHTML("beforeend", filterInputTemplate);

    let removeButton = document.getElementById(`as-remove-filter-${advancedSearchQueriesNumber}`);
    let number = advancedSearchQueriesNumber;
    removeButton.addEventListener("click", () => {
        console.log("Remove: "+ number)
        document.getElementById(`as-filter-container-${number}`).remove();
        filtersIds.delete(number);
        console.log(filtersIds)
    });

    console.log(filtersIds)
}

addFilterButton.addEventListener("click", () => { addPaperFilter(); });


let showAbstract: boolean = (document.getElementById('show-abstract') as HTMLInputElement).checked;
let showAuthors: boolean = (document.getElementById('show-authors') as HTMLInputElement).checked;
let showKeywords: boolean = (document.getElementById('show-keywords') as HTMLInputElement).checked;

document.getElementById('show-abstract').addEventListener('change', () => {
    showAbstract = !showAbstract;

    updatePaperSearchResults();
});

document.getElementById('show-authors').addEventListener('change', () => {
    showAuthors = !showAuthors;

    updatePaperSearchResults();
});

document.getElementById('show-keywords').addEventListener('change', () => {
    showKeywords = !showKeywords;

    updatePaperSearchResults();
});


/*******************   PAPER -> VISUALIZE RESULTS  ************************/

let currentSearchResult: PaperSearchDto | TableSearchDto | null = null;

function updateSearchResults() {
    if (!currentSearchResult) {
        console.log("No search results available. Returned NULL");
        return;
    }

    // Type guard to check if it is PaperSearchDto
    if (isPaperSearchDto(currentSearchResult)) {
        console.log("PAPER RESULTS RECEIVED");
        updatePaperSearchResults();
    } 
    // Type guard to check if it is TableSearchDto
    else if (isTableSearchDto(currentSearchResult)) {
        console.log("TABLE RESULTS RECEIVED");
        updateTableSearchResults();
    }
}

function updateTableSearchResults() {
    let searchResults: TableSearchDto = currentSearchResult as TableSearchDto;

    const queryTimeElement = document.getElementById('query-time');
    if (queryTimeElement) {
        queryTimeElement.textContent = `Query executed in ${searchResults.queryTimeMs} ms, ${searchResults.tables.length} results found.`;
    }

    const suggestionElement = document.getElementById('suggestion');
    if (suggestionElement) {
        if (searchResults.suggestion) {
            suggestionElement.innerHTML = `Did you mean <i>${searchResults.suggestion}</i> ?`;
        }
    }

    const resultsContainer = document.getElementById('results');

    if (!resultsContainer) return;

    resultsContainer.innerHTML = '';

    if (searchResults.tables.length <= 0) {
        resultsContainer.innerHTML = '<p>No results found</p>';
        return;
    }

    searchResults.tables.forEach(table => {
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result-item');

        resultDiv.innerHTML = `
            <div class="my-4">
                <h3 class="my-0" style="font-size: 1.1rem;">
                    [<span>${table.paperId}</span>] <a target="_blank" href="https://ar5iv.labs.arxiv.org/html/${table.paperId}#${table.tableId}" class="text-primary ">${table.tableId}</a> 
                    <span style="font-size: 0.65rem;">[Score: ${table.score.toFixed(2)}]</span>
                </h3>
            </div>
        `;
        resultsContainer.appendChild(resultDiv);
    });
}

function updatePaperSearchResults() {
    let searchResults: PaperSearchDto = currentSearchResult as PaperSearchDto;
    
    const queryTimeElement = document.getElementById('query-time');
    if (queryTimeElement) {
        queryTimeElement.textContent = `Query executed in ${searchResults.queryTimeMs} ms, ${searchResults.documents.length} results found.`;
    }

    const suggestionElement = document.getElementById('suggestion');
    if (suggestionElement) {
        if (searchResults.suggestion) {
            suggestionElement.innerHTML = `Did you mean <i>${searchResults.suggestion}</i> ?`;
        }
    }

    const resultsContainer = document.getElementById('results');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = '';

    if (searchResults.documents.length <= 0) {
        resultsContainer.innerHTML = '<p>No results found</p>';
        return;
    }

    searchResults.documents.forEach(doc => {
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result-item');

        const abstractText = (doc.Abstract ?? "No abstract available.").trim(); 
        let abstractSnippet = "<strong>Abstract: </strong>" + abstractText.split(' ').slice(0, 60).join(' ') + (abstractText.split(' ').length > 60 ? '...' : '');
        
        if (!showAbstract) {
            abstractSnippet = '';
        }

        const authorsText = (doc.Authors ?? "No authors available.").trim(); 
        let authorsSnippet = authorsText.split(' ').slice(0, 15).join(' ') + (authorsText.split(' ').length > 15 ? '...' : '');

        if (!showAuthors) {
            authorsSnippet = '';
        }
        
        let keywordsText = (doc.Keywords ?? "No keywords available.").trim();

        if (!showKeywords) {
            keywordsText = '';
        }

        resultDiv.innerHTML = `
            <div class="my-4">
                <h3 class="my-0" style="font-size: 1.1rem;">
                    [<span>${doc.filename}</span>] <a target="_blank" href="https://arxiv.org/abs/${doc.filename}" class="text-primary ">${doc.Title}</a> 
                    <span style="font-size: 0.65rem;">[Score: ${doc.score.toFixed(2)}]</span>
                </h3>
                <p class="my-0" style="color: #777; font-size: 0.75em;">${keywordsText}</p>
                <p class="my-0" style="font-size: 0.8em;">${authorsSnippet}</p>
                <p class="my-0" style="font-size: 0.9em;">${abstractSnippet}</p>
            </div>
        `;
        resultsContainer.appendChild(resultDiv);
    });
}

/*******************   PAPER -> QUERY  ************************/
function buildPaperAdvancedQuery() {
    let text = (document.getElementById("as-query") as HTMLInputElement).value;
    let filter = (document.getElementById("as-filter") as HTMLSelectElement).value;
    let operator = ""

    function transformText(text: string, filter: string): string {
        filter = filter == "all" ? "" : `${filter}:`;
        const parts = text.match(/"[^"]*"|\S+/g);
    
        const transformedParts = parts?.map(part => { 
            return `${filter}${part}`; 
        });
    
        return transformedParts ? transformedParts.join(' ') : '';
    }

    let query = transformText(text, filter);

    filtersIds.forEach((id) => {
        operator = (document.getElementById(`as-operator-${id}`) as HTMLSelectElement).value.toUpperCase();
        filter = (document.getElementById(`as-filter-${id}`) as HTMLSelectElement).value;
        text = (document.getElementById(`as-query-${id}`) as HTMLInputElement).value;

        query += ` ${operator} ${transformText(text, filter)}`;
    });

    let maxResults = (document.getElementById("as-max-results") as HTMLInputElement).value;
    return query + `&numberOfResults=${maxResults}`;
}

document.getElementById("as-search-button").addEventListener("click", () => {
    let query = buildPaperAdvancedQuery();

    sendQuery(query);
});

function sendQuery(query: string) {
    console.log(query)

    let url = "http://localhost:3000/api/search/" + currentSearchType;

    document.getElementById('search-result').classList.remove("d-none");

    axios.get(`${url}?query=${query}`).then((response) => {
        console.log(response.data);

        currentSearchResult = response.data;
        
        updateSearchResults();

    }).catch((error) => {
        console.error('Error fetching search results:', error);
        const resultsContainer = document.getElementById('results');
        if (resultsContainer) {
            resultsContainer.innerHTML = '<p>Error fetching results. Please try again later.</p>';
        }
    });
}
