$(document).ready(function() {
    // Toggle chatbox visibility
    $('#chatbot-button').click(function() {
        $('#chatbox-container').toggleClass('open');
    });

    // Send user message
    $('#send-button').click(function() {
        sendMessage();
    });

    // Send message on Enter key press
    $('#user-input').keypress(function(event) {
        if (event.which === 13) {  // Enter key
            sendMessage();
        }
    });

    function sendMessage() {
        var userInput = $('#user-input').val().trim();
        if (userInput === "") return;

        $('#chatbox').append('<div class="user-message">' + userInput + '</div><div class="clearfix"></div>');
        $('#user-input').val('');  // Clear input

        // Send query to backend and get bot response
        $.ajax({
            url: '/ask/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: userInput }), // Ensure data is correctly formatted
            success: function(data) {
                $('#chatbox').append('<div class="bot-response">' + data.response + '</div><div class="clearfix"></div>');
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);  // Scroll to bottom
            },
            error: function(xhr) {
                $('#chatbox').append('<div class="bot-response">Error: ' + xhr.responseText + '</div><div class="clearfix"></div>');
            }
        });        
    }
});