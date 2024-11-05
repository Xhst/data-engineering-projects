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

function sendQuery(query: string) {
    console.log(query)
    axios.get(`http://localhost:3000/api/search?query=${query}`).then((response) => {
        console.log(response.data);
    });
}
