$(document).ready(function() {
    $('#chatForm').on('submit', function(event) {
        event.preventDefault();
        var query = $('#query').val();
        $.ajax({
            url: '/chat',
            type: 'POST',
            data: { query: query },
            success: function(response) {
                // Access the 'response' field of the JSON object and display it
                $('#response').html('<pre>' + response.response + '</pre>');
            },
            error: function(xhr, status, error) {
                // Handle errors
                $('#response').html('<pre>Error: ' + error + '</pre>');
            }
        });
    });
});
