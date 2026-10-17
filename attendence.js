
const form = document.getElementById("attendanceForm");


form.addEventListener("submit", function(event) {

    const attended = Number(
        document.getElementById("attended").value
    );

    const total = Number(
        document.getElementById("total").value
    );


    // Classes attended cannot be negative

    if (attended < 0) {

        event.preventDefault();

        alert("Classes attended cannot be negative");

        return;
    }


    // Total classes must be greater than 0

    if (total <= 0) {

        event.preventDefault();

        alert("Total classes must be greater than 0");

        return;
    }


    // Attended cannot exceed total

    if (attended > total) {

        event.preventDefault();

        alert(
            "Classes attended cannot be greater than total classes"
        );

        return;
    }

});