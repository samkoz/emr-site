$(document).ready(function(){
  $(".delete_button").click(function(){
      console.log("button clicked");
      var entry_id = this.id;

      // test to make sure entry_id works
      console.log(entry_id);

      // test to make sure identifying appropriate row
      var test = $("tr#" + entry_id).html();
      console.log(test);

      // successfully deletes it from the DOM
      $("tr#" + entry_id).remove()

      $.ajax({
        url: '/view_profile',
        data: {"entry_id" : entry_id},
        type: 'POST',
        success: function(response){
          console.log(response);
        },
        error: function(error) {
          console.log(error);
        }
    });
  });
});
