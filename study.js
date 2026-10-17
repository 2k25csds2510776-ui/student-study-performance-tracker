// Get the Study Form
const form = document.getElementById("studyForm");


// Run when the form is submitted
form.addEventListener("submit", function(event) {

    // Get study hours
    const hours = Number(
        document.getElementById("hours").value
    );


    // Check if hours are valid
    if (hours <= 0) {

        // Stop form from going to Flask
        const form = document.getElementById("studyForm");

        form.addEventListener("submit", function(event) {

        const hours = Number(
            document.getElementById("hours").value
        );

        if (hours <= 0) {

            event.preventDefault();

            alert("Study hours must be greater than 0");

            return;
        }

        });

        alert(
            "Study hours must be greater than 0"
        );

        return;
    }

});