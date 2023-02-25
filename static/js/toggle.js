$(document).ready(function() {
  $('#toggle').on('change', function() {
    console.log("HERE")
    if ($(this).is(':checked')) {
      $('#toggle-label').text('Yes');
      $('#toggle-input').val('Yes');
    } else {
      $('#toggle-label').text('No');
      $('#toggle-input').val('No');
    }
  });


    $("#searchInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $(".dropdown-menu .form-check").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });

    $("#searchInput").on("keyup", function() {
      var query = $(this).val().toLowerCase(); // Get the search query
      var items = $(".dropdown-menu .form-check"); // Get all the items in the dropdown menu
      var hasResults = false; // Flag to check if there are any results
  
      // Loop through the items and show/hide them based on the search query
      items.each(function() {
        var itemText = $(this).text().toLowerCase();
        if (itemText.includes(query)) {
          $(this).show();
          hasResults = true;
        } else {
          $(this).hide();
        }
      });
  
      // Show/hide the dropdown menu based on the search query
      if (hasResults) {
        $(".dropdown-menu").show();
      } else {
        $(".dropdown-menu").hide();
      }
    });

    $('.dropdown-toggle').click(function() {
      $('.dropdown-menu').toggle();
    });
  
    // Hide dropdown menu when clicked outside
    $(document).click(function(event) {
      var target = $(event.target);
      if (!target.hasClass('dropdown-toggle') && !target.hasClass('dropdown-menu')) {
        $('.dropdown-menu').hide();
      }
    });

    $('#dropdownMenuButton').on('shown.bs.dropdown', function() {
      $('#searchInput').focus();
    });
  
    $('.dropdown-menu').on('click', function(e) {
      e.stopPropagation();
    });
  
    $('#searchInput').on('keyup', function() {
      var value = $(this).val().toLowerCase();
      $('.dropdown-menu .form-check').filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
    
    $('.form-check-input').on('click', function(e) {
      e.stopPropagation();
    });

});
/*
document.getElementById("searchInput").addEventListener("keyup", search);

function search() {
  // Get the search query
  var query = document.getElementById("searchInput").value.toLowerCase();

  // Get all the items in the dropdown menu
  var items = document.querySelectorAll(".dropdown-item");

  // Loop through the items and hide/show them based on the search query
  for (var i = 0; i < items.length; i++) {
    var itemText = items[i].textContent.toLowerCase();
    if (itemText.includes(query)) {
      items[i].style.display = "block";
    } else {
      items[i].style.display = "none";
    }
  }

  // Show the dropdown menu
  document.getElementById("dropdownMenuButton").click();
}*/