function form_search(){
    newURI = "http://realitycheck.pl/search/" + encodeURI($('#searchfield').val()) + "/";
    //console.log(newURI);
    window.location.href = newURI;
}