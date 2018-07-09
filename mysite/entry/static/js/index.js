
var engToBhut = document.getElementById("engToBhut");
var bhutToEng = document.getElementById("bhutToEng");
var tibToBhut = document.getElementById("tibToBhut");


/*
engToBhut.addEventListener("click", change(engToBhut.value));
bhutToEng.addEventListener("click", change(bhutToEng.value));
sansToBhut.addEventListener("click", change(sansToBhut.value));



*/

/*
function random(number) {
  return Math.floor(Math.random()*number);
}
function bgChange(e) {
  var rndCol = 'rgb(' + random(255) + ',' + random(255) + ',' + random(255) + ')';
  e.target.style.backgroundColor = rndCol;
  event.stopPropagation();
  console.log(e);
}
*/
engToBhut.onclick =  function() {
  document.myform.setAttribute("action", "/entry/english_bhutia/");
  console.log("1");
}
bhutToEng.onclick =  function() {
  document.myform.setAttribute("action", "/entry/bhutia_english/");
  console.log("2");
}
tibToBhut.onclick =  function() {
    document.myform.setAttribute("action", "/entry/tibetan_bhutia/");
  console.log("3");
}
