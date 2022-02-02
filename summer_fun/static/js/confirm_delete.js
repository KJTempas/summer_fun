var deleteButtons = document.querySelectorAll('.delete');

deleteButtons.forEach(function(button){

  button.addEventListener('click', function(ev){

    // Show a confirm dialog
    var okToDelete = confirm("Delete activity - are you sure? Students will no longer be able to select this activity, but if already signed up, it will remain on their schedule.");

    // If user presses no/cancel, prevent the form submit
    if (!okToDelete) {
      ev.preventDefault();  // Prevent the click event propagating
    }

    // Otherwise, the web page will continue processing the event, 
    // and send the delete request to the server.


  })
});