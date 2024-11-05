import axios from "axios";

let advancedSearchQueriesNumber = 0;

let filtersIds: Set<number> = new Set();

function addFilter() {
    advancedSearchQueriesNumber++;

    filtersIds.add(advancedSearchQueriesNumber);

    let filterInputTemplate = `
        <div id="as-filter-container-${advancedSearchQueriesNumber}" class="input-group mb-3">
            <select class="form-select" id="as-operator-${advancedSearchQueriesNumber}"
                style="max-width: 90px">
                <option value="and" selected>AND</option>
                <option value="or">OR</option>
                <option value="not">NOT</option>
            </select>
            <input type="text" class="form-control" aria-label="Text input with dropdown button">
            <select class="form-select" id="as-filter-${advancedSearchQueriesNumber}"
                style="max-width: 120px">
                <option value="1" selected>All</option>
                <option value="2">Title</option>
                <option value="3">Abstract</option>
                <option value="3">Keywords</option>
                <option value="3">Authors</option>
            </select>
            <button class="btn btn-outline-danger" id="as-remove-filter-${advancedSearchQueriesNumber}"><i class="bi bi-x"></i></button>
        </div>
        `;
    
        document.getElementById("as-filters-container").insertAdjacentHTML("beforeend", filterInputTemplate);

    const removeButton = document.getElementById(`as-remove-filter-${advancedSearchQueriesNumber}`);
    removeButton.addEventListener("click", () => {
        document.getElementById(`as-filter-container-${advancedSearchQueriesNumber}`).remove();
        filtersIds.delete(advancedSearchQueriesNumber);
    });

    console.log(filtersIds);
}

document.getElementById("as-add-filter-button").addEventListener("click", () => { addFilter(); });
/*
axios.get("http://localhost:3000/api/search?query=AAA").then((response) => {
    console.log(response.data);
});
*/