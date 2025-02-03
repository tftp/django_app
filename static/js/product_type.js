
let elm = document.getElementById("prt");
let elPrts = document.getElementsByClassName("producttype");
let tot = document.getElementById("total");
let pdf = document.getElementById("pdf");


let typePr = {}

for (let i=0; i<elPrts["length"];++i) {
    let num = elPrts[i].dataset.id;
    typePr[num] = elPrts[i].innerText;
}


for (let key in typePr) {
    elA = document.createElement('a');
    elA.innerText = typePr[key];
    elA.className = "badge rounded-pill bg-success";
    elA.dataset.id = key;
    elA.onclick = toggle;
    elm.appendChild(elA);
    elSp2 = document.createElement('span');
    elSp2.innerText = '\u00A0';
    elm.appendChild(elSp2);
}

function toggle(event) {
    let elem = event.target;
    let typeId = elem.dataset.id;
    pdf.href = `download/?type=${elem.innerText}`;
    for (let i=0; i<elPrts["length"];++i) {
        if (elPrts[i].dataset.id == typeId) {
            elPrts[i].parentNode.parentNode.hidden = false;
        } else {
            elPrts[i].parentNode.parentNode.hidden = true;
        }
    }
    countPrts();
}

function countPrts() {
    let cnt = 0;
    for (let i=0; i<elPrts["length"];++i) {
        if (elPrts[i].parentNode.parentNode.hidden == false) {
            cnt += 1;
        }
    }
    tot.innerText = `Итого: ${cnt}`;
}