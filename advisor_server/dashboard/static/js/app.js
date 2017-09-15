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
                    // TODO: do not redirect to another page once success
                    //window.location.href = document.URL;
                },
                error: function(data) {
                    alert(data.message);
                }
            });
        }
  }
