
var now = new Date();
var day = ("0" + now.getDate()).slice(-2);
var month = ("0" + (now.getMonth() + 1)).slice(-2);
var today = (month)+"/"+(day)+"/"+now.getFullYear();


function getTasks(date) {
	var http = new XMLHttpRequest();
	var url = "/tasks";
	if (date==null){
		var params = {"date": (now.getFullYear()+"-"+(month)+"-"+(day))};	
	} else {
		var params = {"date":date};
	}
	
	http.open("GET", url, true);
	var taskList = document.getElementById("taskGroup");
	taskList.innerHTML = "";
	document.getElementById("sidebar").classList.remove("active");
	document.getElementById("loading").style.display = 'block';

	http.onreadystatechange = function() {
	    if(http.readyState == 4 && http.status == 200) {
	    	//console.log(http.responseText);
	    	var task = http.responseText;
	        var taskList = document.getElementById("taskGroup");

	        document.getElementById("loading").style.display = 'none';
	        taskList.innerHTML = task;
	        document.getElementById("tasksDiv").style.display = 'block';
	    }
	}
	http.send(params);
}

// init datepicker, sidebar, getTasks on page load
$(document).ready(function() {
	$( "#enddate" ).datepicker();
	$( "#enddate" ).val(today);
	getTasks((now.getFullYear()+"-"+(month)+"-"+(day)));
	// sidebar stuff
	$('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

    //
    $("#tasksSel").on('click', function(){
    	document.getElementById("callsDiv").style.display = 'none';
    	document.getElementById("tasksDiv").style.display = 'block';

    	document.getElementById("tasksLi").classList.add("active");
    	document.getElementById("callsLi").classList.remove("active");

    	document.getElementById("activePage").innerHTML = "Tasks";

    	$('#sidebar').toggleClass('active');
    })

    $("#callsSel").on('click', function(){
    	document.getElementById("tasksDiv").style.display = 'none';
    	document.getElementById("callsDiv").style.display = 'block';

    	document.getElementById("callsLi").classList.add("active");
    	document.getElementById("tasksLi").classList.remove("active");

    	document.getElementById("activePage").innerHTML = "Calls";

    	$('#sidebar').toggleClass('active');
    })

    $(document.body).swipe( {
    	swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
      		console.log("You swiped " + direction + " count: " + fingerCount);

      		if (fingerCount == 2){
      			if (direction == "left"){
    				document.getElementById("sidebar").classList.remove("active");
      			}

      			if (direction == "right"){
      				document.getElementById("sidebar").classList.add("active");
    	
      			}
      		}
      		
      	}
    } );



});

// getTasks when updated date
$("#enddate").change(function(){ 
	var selDate = $.datepicker.formatDate("yy-mm-dd", $('#enddate').datepicker("getDate"));
    getTasks(selDate);
})

// following links on webapp ios
var a=document.getElementsByTagName("a");
for(var i=0;i<a.length;i++)
{
    a[i].onclick=function()
    {
        window.location=this.getAttribute("href");
        return false
    }
}


