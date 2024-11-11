import axios from "axios";

type Theme = 'light' | 'dark';

let currentTheme: Theme = 'light';

console.log(
    '🚀 Developed by %c 🌲 Xhst, Prox, Diggi 🌲',
    'color: green; font-weight: bold;'
);

let advancedSearchQueriesNumber = 0;
let addFilterButton = document.getElementById("as-add-filter-button")

let filtersIds: Set<number> = new Set();

function addFilter() {
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

addFilterButton.addEventListener("click", () => { addFilter(); });

function buildAdvancedQuery() {
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
    let query = buildAdvancedQuery();

    sendQuery(query);
});

let searchInput = document.getElementById("search") as HTMLInputElement;

searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        let query = searchInput.value;

        sendQuery(query);
    }
});

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

interface DocumentDto {
    filename: string;
    Title: string;
    Authors: string | null;
    Keywords: string | null;
    Abstract: string | null;
    score: number;
}

interface SearchDto {
    documents: DocumentDto[];
    suggestion: string | null;
    queryTimeMs: number;
}

let showAbstract: boolean = (document.getElementById('show-abstract') as HTMLInputElement).checked;
let showAuthors: boolean = (document.getElementById('show-authors') as HTMLInputElement).checked;
let showKeywords: boolean = (document.getElementById('show-keywords') as HTMLInputElement).checked;

document.getElementById('show-abstract').addEventListener('change', () => {
    showAbstract = !showAbstract;

    updateSearchResults();
});

document.getElementById('show-authors').addEventListener('change', () => {
    showAuthors = !showAuthors;

    updateSearchResults();
});

document.getElementById('show-keywords').addEventListener('change', () => {
    showKeywords = !showKeywords;

    updateSearchResults();
});

let currentSearchResult: SearchDto | null = null;

function updateSearchResults() {
    const data = currentSearchResult;
    
    console.log(data);

    if (!data) return;

    const queryTimeElement = document.getElementById('query-time');
    if (queryTimeElement) {
        queryTimeElement.textContent = `Query executed in ${data.queryTimeMs} ms, ${data.documents.length} results found.`;
    }

    const suggestionElement = document.getElementById('suggestion');
    if (suggestionElement) {
        if (data.suggestion) {
            suggestionElement.innerHTML = `Did you mean <i>${data.suggestion}</i> ?`;
        }
    }

    const resultsContainer = document.getElementById('results');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';

        if (data.documents.length > 0) {
            data.documents.forEach(doc => {
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
        } else {
            resultsContainer.innerHTML = '<p>No results found</p>';
        }
    }
}

function sendQuery(query: string) {
    console.log(query)

    document.getElementById('search-result').style.display = 'block';

    axios.get(`http://localhost:3000/api/search?query=${query}`).then((response) => {
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