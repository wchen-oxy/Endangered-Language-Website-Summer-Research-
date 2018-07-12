
document.addEventListener('DOMContentLoaded',function() {
    document.querySelector('select[name="translation"]').onchange=changeEventHandler;
},false);

function changeEventHandler(event) {
    // You can use “this” to refer to the selected element.


    if(event.target.value == "engToBhut") document.myform.setAttribute("action", "/entry/english_bhutia/");

    if (event.target.value == "bhutToEng") document.myform.setAttribute("action", "/entry/bhutia_english/");

    if (event.target.value == "tibToBhut")   document.myform.setAttribute("action", "/entry/tibetan_bhutia/");

}
