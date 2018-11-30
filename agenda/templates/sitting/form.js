function confirm(event) {
    // event.preventDefault();
    document.getElementById("confirmation").style.display = "block";
    return false;
};

function addTable() {

    var newTableField = document.createElement("LI");
    selectNode = `
             <input type="number" name="tables" min="1" max="100" value="1">

    `;
    newTableField.innerHTML = selectNode;

    var table_list = document.getElementById("table-list");
    table_list.insertBefore(newTableField, document.getElementById("add-table-li"));
}
