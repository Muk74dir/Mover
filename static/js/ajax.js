$(document).ready(function () {
    $(".add-destination-button").on("click", function () {
      // Collect form data
      var destinationAddress = $("#destination-address-input").val();
      var travelMode = $("input[name='travel-mode']:checked").val();

      // Create an object with the data
      var formData = {
        'destination-address': destinationAddress,
        'travel-mode': travelMode,
        // Add other form fields as needed
      };

      // Perform AJAX request
      $.ajax({
        type: "POST",
        url: "/distance/",
        data: formData,
        beforeSend: function (xhr, settings) {
          // Include CSRF token in the headers
          xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
        },
        success: function (response) {
          // Handle success response from the server
          console.log("Data sent successfully:", response);
        },
        error: function (error) {
          // Handle error
          console.error("Error sending data:", error);
        },
      });
    });
  });