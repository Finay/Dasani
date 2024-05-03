window.onload = function(){
    var open = true;
    setTimeout(function(){
    document.getElementById("closer").addEventListener("click", function(){
        open = !open;
        if (open) {
            document.getElementById("close").style.setProperty("opacity", 1);
            document.documentElement.style.setProperty('--split', '70%');
        } else {
            document.getElementById("close").style.setProperty("opacity", 0);
            document.documentElement.style.setProperty('--split', '93%');
        }
    })}, 4000);
}