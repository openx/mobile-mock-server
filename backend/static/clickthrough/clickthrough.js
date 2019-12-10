//Have the "time" p tag say what the current dateTime is.
window.onload = function(){
    var d = new Date();
    document.getElementById("time_tag").innerHTML = d;
}
