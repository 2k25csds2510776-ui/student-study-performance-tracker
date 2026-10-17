const form = document.getElementById("marksForm");

form.addEventListener("submit", function(event) {

    const marks = Number(
        document.getElementById("marks").value
    );

    const total = Number(
        document.getElementById("total").value
    );


    // Marks cannot be negative

    if (marks < 0) {

        event.preventDefault();

        alert("Marks cannot be negative");

        return;
    }


    // Total must be greater than 0

    if (total <= 0) {

        event.preventDefault();

        alert("Total marks must be greater than 0");

        return;
    }


    // Marks cannot exceed total

    if (marks > total) {

        event.preventDefault();

        alert(
            "Marks obtained cannot be greater than total marks"
        );

        return;
    }

});