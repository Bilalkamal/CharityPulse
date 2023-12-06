$(document).ready(function(){
    $("#einForm").submit(function(event){
        event.preventDefault();
        var ein = $("#ein").val();
        $.ajax({
            url: 'http://127.0.0.1:5000/lookup',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ ein: ein }),
            success: function(response){
                console.log(response);
                displayResults(response);
            },
            error: function(error){
                console.log(error);
                $("#result").html("Error: " + error.responseText);
            }
        });
    });

    function displayResults(data){
        var resultHtml = "<h2>Charity Information</h2>";
        $.each(data, function(key, value){
            resultHtml += "<p><strong>" + key + ":</strong> " + value + "</p>";
        });
        $("#result").html(resultHtml);
        $("#result").show(); // Show the results div
    }
});
