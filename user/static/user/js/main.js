function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).ready(function () {
  $(".characterWindow").click(function () {
    console.log($(this).attr("value"));
    console.log(getCookie("csrftoken"));

    $.ajax({
      type: "GET",
      url: "api/",
      headers: {
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },

      data: {
        character_name: $(this).attr("value"),
      },

      success: function (response) {

        console.log(response.message);

        // Tu pol naprej updejtaš html ...
      },
      error: function (response) {
        // alert the error if any error occured
      },
    });
  });
});
