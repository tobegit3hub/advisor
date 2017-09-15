
function delete_resource(url) {
     if (confirm('Do you want to delete the resource?')) {
             $.ajax({
                url: url,
                type: 'DELETE',
                dataType: "json",
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                },
                success: function(data) {
                    // TODO: Do not redirect to another page once success
                    //window.location.href = document.URL;
                },
                error: function(data) {
                    //TODO: Should not get error here
                    //alert(data.message);
                }
            });
        }
  }

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
