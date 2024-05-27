// custom.js

// JavaScript code for sending mail using AJAX
function sendMail(pk) {
    $.ajax({
        url: `/send-mail/${pk}/`,
        type: 'GET',
        success: function(response) {
            if (response.status === 'success') {
                // Update the status on the page dynamically
                $('#status').text('Email Sent');
                // Show success message to the user
                alert(response.message);
            } else {
                // Show error message to the user
                alert(response.message);
            }
        },
        error: function(xhr, status, error) {
            // Show error message to the user
            alert('Error sending email: ' + error);
        }
    });
}
