function minID(div_array){
  console.log(div_array);
  var min = parseInt(div_array[0].id);
  for (var i = 1; i <= div_array.length-1; i++) {
    if(parseInt(div_array[i].id)<min){
      min = parseInt(div_array[i].id);
    }
  }
  return min;
}
function loadNext(){
  var divs = $('.post-container');
  var lastID = minID(divs);
  console.log(lastID);
  //var request = $.ajax("getNextPost/"+(lastID+1));
  //for (var i = 0; i < 3; i++) {
    if(lastID>1){
      $('#more_button').text("Loading ...");
      $('#more_button').prop("disabled", true);
      $.ajax({
        type : "GET",
        url : "/getNextPost/"+(lastID-1)
      }).done(function(data, textStatus, jqXHR) {
        var b = $('body');
        var newEl = b.append(data);
        $('#more_button').insertAfter(newEl);
        //activate flattr button
        FlattrLoader.setup();
        //return data;
      }).fail(function(jqXHR, textStatus) {
        console.log(textStatus);
        //return null;
      });
      $('#more_button').text("Load Moarrrr ...");
      $('#more_button').prop("disabled", false);
    }
    else{
      $('#more_button').text("No more posts available");
      $('#more_button').prop("disabled", true);
      //return data;
      i=3;
    }
    //lastID--;
  //}
}