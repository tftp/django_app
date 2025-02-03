
let elSwitch = document.getElementById("archivedSwitchCheck");
let elArchived = document.getElementsByClassName("table-danger");

elSwitch.onchange = toggle;

function toggle(event) {
    let elem = event.target;
    let stage = elem.checked;
    for (let i=0; i<elArchived["length"];++i) {
        if (stage) {
            elArchived[i].hidden = true;
        } else {
            elArchived[i].hidden = false;
        }
    }
}
