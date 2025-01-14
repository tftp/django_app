
let elSwitch = document.getElementById("flexSwitchCheckDefault");
let elCstmrs = document.getElementsByClassName("table-danger");

elSwitch.onchange = toggle;

function toggle(event) {
    let elem = event.target;
    let stage = elem.checked;
    for (let i=0; i<elCstmrs["length"];++i) {
        if (stage) {
            elCstmrs[i].hidden = true;
        } else {
            elCstmrs[i].hidden = false;
        }
    }
}
