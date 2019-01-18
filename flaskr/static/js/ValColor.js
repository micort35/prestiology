$(document).ready(function() {
    var tbl = document.getElementById("results");
    const rows = tbl.rows;
    const rowCt = rows.length;
    for(var i = 0; i < rowCt; i++){
        const cells = rows[i].cells;
        const cellCt = cells.length;
        for(var j = 0; j < cellCt; j++){
            var val = cells[j].textContent;
            var cName = cells[j].className;
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