$(document).ready(function() {
    const tbl = document.getElementById('results');
    const rows = tbl.rows;
    const rowCt = rows.length;
    for(let i = 0; i < rowCt; i++){
        const cells = rows[i].cells;
        const cellCt = cells.length;
        for(let j = 0; j < cellCt; j++){
            const val = cells[j].textContent;
            const cName = cells[j].className;
            if(cName == "valcolored"){
                if(val >= 2){
                    cells[j].style.backgroundColor = "#29BF12";
                } else if(val >= 1){
                    cells[j].style.backgroundColor = "#ABFF4F";
                } else if(val <= -2){
                    cells[j].style.backgroundColor = "#D62246";
                } else if(val <= -1){
                    cells[j].style.backgroundColor = "#DB5375";
                }
            }
        }
    }
})