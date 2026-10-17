// Get form
const form = document.getElementById("assignmentForm");

// Get table
const table = document.getElementById("assignmentTable");


// Run when form is submitted
form.addEventListener("submit", function(event) {

    // Prevent page refresh
    event.preventDefault();


    // Get values from form
    const subject =
        document.getElementById("subject").value;

    const assignment =
        document.getElementById("assignment").value;

    const dueDate =
        document.getElementById("dueDate").value;

    const status =
        document.getElementById("status").value;

    const semester =
        document.getElementById("semester").value;


    // Create new row
    const row = table.insertRow(-1);


    // Add data to row
    row.insertCell(0).textContent = subject;

    row.insertCell(1).textContent = assignment;

    row.insertCell(2).textContent = dueDate;

    row.insertCell(3).textContent = status;

    row.insertCell(4).textContent =
        "Semester " + semester;


    // Clear form
    form.reset();

});