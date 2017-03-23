$(document).ready(function(){
  $(".delete_button").click(function(){
      var entry_id = this.id;
      var entry_class = this.className;
      var entry_type = ""
      if (entry_class.indexOf('saved_entries') !== -1) {
        entry_type = 'saved';
      } else {
        entry_type = "submission";
      }
      // successfully deletes it from the DOM
      $("tr#" + entry_id).remove()

      $.ajax({
        url: '/view_profile',
        data: {"entry_id" : entry_id, "entry_type" : entry_type},
        type: 'POST',
        success: function(response){
          console.log(response);
        },
        error: function(error) {
          console.log(error);
        }
      });
  });

  $(".save.button").click(function(){
    console.log("button clicked");
    var entry_id = this.id;

    $.ajax({
      url: '/show_entries',
      data: {"entry_id" : entry_id},
      type: 'POST',
      success: function(response){
        var json = JSON.parse(response);
        var status = json['status'];
        var data = json['data']
        var message = data[0]
        var num_saves = data[1]
        console.log(message)
        if (status == 'Error') {
          $("#error_message").text(function(){
            return message;
          })
          // this won't work for some reason...
          $("p#" + entry_id).text(function(){
            return message;
          })
        } else {
          $( "td.num_saves#" + entry_id).text(function(){
            return num_saves;
          })
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});
