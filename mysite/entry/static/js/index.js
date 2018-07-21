
//add listeners
document.addEventListener('DOMContentLoaded',function() {
  document.querySelector('select[name="translation"]').onchange=changeEventHandler;
},false);

//code for things that need to be run each time the page is run
window.onload = function() {

  var selected = document.createAttribute("selected");
  if (localStorage.getItem("storageName")) {
    var thing = localStorage.getItem("storageName");
    var element = document.getElementById(thing);

    if (thing == "be") {
      document.myform.setAttribute("action","/entry/bhutia_english/");};
      if (thing == "eb") {document.myform.setAttribute("action", "/entry/english_bhutia/");
      element.setAttribute("selected", "selected");};
      if (thing == "tb") {document.myform.setAttribute("action", "/entry/tibetan_bhutia/");
      element.setAttribute("selected", "selected");
    };}
    console.log(document.getElementById("translation"));

  }

  //code that is only run when a change is detected
  function changeEventHandler(event) {
    if (event.target.value == "bhutToEng") {
      document.myform.setAttribute("action", "/entry/bhutia_english/");
      localStorage.setItem("storageName", "be");

    }
    if(event.target.value == "engToBhut") {
      document.myform.setAttribute("action", "/entry/english_bhutia/");
      localStorage.setItem("storageName", "eb");

    }

    if (event.target.value == "tibToBhut")  { document.myform.setAttribute("action", "/entry/tibetan_bhutia/");
    localStorage.setItem("storageName", "tb");
  }
}
