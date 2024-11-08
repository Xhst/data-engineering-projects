import axios from "axios";

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

    filter = filter === "all" ? "" : filter + ":";

    let query = `${filter}${text}`

    filtersIds.forEach((id) => {
        operator = (document.getElementById(`as-operator-${id}`) as HTMLSelectElement).value.toUpperCase();
        filter = (document.getElementById(`as-filter-${id}`) as HTMLSelectElement).value;
        text = (document.getElementById(`as-query-${id}`) as HTMLInputElement).value;

        filter = filter === "all" ? "" : filter + ":";

        if (text === "") return;

        query += ` ${operator} ${filter}${text}`;
    });

    return query;
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

function sendQuery(query: string) {
    console.log(query)

    axios.get(`http://localhost:3000/api/search?query=${query}`).then((response) => {
        console.log(response.data);
        const data: SearchDto = response.data;

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
                    const abstractSnippet = abstractText.split(' ').slice(0, 60).join(' ') + (abstractText.split(' ').length > 60 ? '...' : '');
                    
                    const authorsText = (doc.Authors ?? "No authors available.").trim(); 
                    const authorsSnippet = authorsText.split(' ').slice(0, 15).join(' ') + (authorsText.split(' ').length > 15 ? '...' : '');
                    
                    const keywordsText = (doc.Keywords ?? "No keywords available.").trim();

                    resultDiv.innerHTML = `
                        <div class="my-4">
                            <h3 class="my-0" style="font-size: 1.1rem;">
                                [<span>${doc.filename}</span>] <a target="_blank" href="https://arxiv.org/abs/${doc.filename}" class="text-primary ">${doc.Title}</a> 
                                <span style="font-size: 0.65rem;">[Score: ${doc.score.toFixed(2)}]</span>
                            </h3>
                            <p class="my-0" style="color: #777; font-size: 0.75em;">${keywordsText}</p>
                            <p class="my-0" style="font-size: 0.8em;">${authorsSnippet}</p>
                            <p class="my-0" style="font-size: 0.9em;"><strong>Abstract: </strong>${abstractSnippet}</p>
                        </div>
                    `;
                    resultsContainer.appendChild(resultDiv);
                });
            } else {
                resultsContainer.innerHTML = '<p>No results found</p>';
            }
        }
    }).catch((error) => {
        console.error('Error fetching search results:', error);
        const resultsContainer = document.getElementById('results');
        if (resultsContainer) {
            resultsContainer.innerHTML = '<p>Error fetching results. Please try again later.</p>';
        }
    });
}