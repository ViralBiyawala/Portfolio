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
    
        // Create a new div and safely insert the user's message
        var userMessageDiv = $('<div class="user-message"></div>').text(userInput);
        $('#chatbox').append(userMessageDiv).append('<div class="clearfix"></div>');
    
        $('#user-input').val('');  // Clear input
    
        // Send query to backend and get bot response
        $.ajax({
            url: '/ask/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: userInput }), // Ensure data is correctly formatted
            success: function(data) {
                // Safely insert bot response as text
                var botResponseDiv = $('<div class="bot-response"></div>').text(data.response);
                $('#chatbox').append(botResponseDiv).append('<div class="clearfix"></div>');
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);  // Scroll to bottom
            },
            error: function(xhr) {
                var errorMessageDiv = $('<div class="bot-response"></div>').text('Error: ' + xhr.responseText);
                $('#chatbox').append(errorMessageDiv).append('<div class="clearfix"></div>');
            }
        });        
    }    
});