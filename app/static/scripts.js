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
        url: 'url_for(routes.view_profile)',
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
      data: {"save_entry" : entry_id},
      type: 'POST',
      success: function(response){
        var json = JSON.parse(response);
        var status = json['status'];
        var data = json['data']
        var message = data[0]
        var num_saves = data[1]
        console.log(message)
        if (status == 'Error') {
            alert(message)
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

  $("a.expand_link").click(function(){
    var template_id = this.id
    var current_template = $("span#" + template_id).text()
    $.ajax({
      url: '/show_entries',
      data: {'update_template': template_id, 'current_template' : current_template},
      type: 'POST',
      success: function(response){
        var json = JSON.parse(response)
        var return_template = json['return_template']
        var action = json['action']
        $("span#" + template_id).text(return_template)
        if (action == 'expand') {
          $('a.expand_link#' + template_id).text('\n(show less)')
          $('button.copybutton.too_long#' + template_id).removeClass("disabled")
        } else {
          $('a.expand_link#' + template_id).text('...(show more)')
          $('button.copybutton.too_long#' + template_id).addClass("disabled")
        }
        console.log(action)
      },
      error: function(error){
        console.log(error)
      }
    })
  })
});
