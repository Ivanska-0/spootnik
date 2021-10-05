var year = false, duration = false;

$(document).ready(function () {
    /**
     * Parser para "Año"
     */
    $("#year").change(function () {
        var y = $("#year").val();
        if (y != "") {
            y = parseInt(y);
            if (!y || y < 1895) {
                $("#year_err").html(" Año inválido");
                year = false;
            }
            else {
                $("#year_err").html("");
                year = true
            }
        }
        else {
            $("#year_err").html("");
            year = true;
        }
    });

    /**
     * Parser para "duración"
     */
    $("#duration").change(function () {
        var d = $("#duration").val();
        if (d == "" || /\d\d:\d\d$/.test(d) || /\d:\d\d$/.test(d)) {
            $("#duration_err").html("");
            duration = true;
        }
        else {
            $("#duration_err").html(" Duración inválida");
            duration = false;
        }
    });
});


/*
function checkEmpty(option) {
    if (option == 1) {
        if ($("#title").val() == "" &&
            $("#year").val() == "" &&
            ($("#genre").children("option:selected").val() == "") ||
             $("#genre").children("option:selected").val() == "all") {
                alert("Introduzca al menos un dato de búsqueda");
                return false;
            }
   }
}
*/