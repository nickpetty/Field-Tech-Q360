var http = new XMLHttpRequest();
var url = "https://360.southcentralav.com/ajax/?_a=authenticate&_r=action=%3Dlogin";
var params = "userid=npetty&password=Scav01234&touch=false&shared=";

http.open("POST", url, true);

http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");



http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
        alert(http.responseText);
    }
}
http.send(params);

console.log(http.responseText);

