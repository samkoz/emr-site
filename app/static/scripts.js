$(document).ready(function(){
    $(".delete_button").click(function(){
        console.log("button clicked");
        var entry_id = this.id;

        // test to make sure entry_id works
        console.log(entry_id);

        // test to make sure identifying appropriate row
        var test = $("tr#" + entry_id).html();
        console.log(test);

        $("tr#" + entry_id).remove()
        // now find a way to delete it

        // then find a way to delete the entry from the database
    });
});
