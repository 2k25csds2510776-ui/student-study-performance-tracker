// Get the form
const form = document.getElementById("examForm");


// Get the table
const table = document.getElementById("examTable");


// Run when Add Exam button is clicked
form.addEventListener("submit", function(event) {

    // Prevent page refresh
    event.preventDefault();


    // Get values from form

    const subject =
        document.getElementById("subject").value;

    const examName =
        document.getElementById("examName").value;

    const examDate =
        document.getElementById("examDate").value;

    const semester =
        document.getElementById("semester").value;


    // Create new row

    const row = table.insertRow(-1);


    // Add values to table

    row.insertCell(0).textContent = subject;

    row.insertCell(1).textContent = examName;

    row.insertCell(2).textContent = examDate;

    row.insertCell(3).textContent =
        "Semester " + semester;


    // Clear form

    form.reset();

});