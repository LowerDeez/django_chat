$(document).ready( function() {
    var objDiv = document.getElementById("div-chat");
    objDiv.scrollTop = objDiv.scrollHeight;
    var editable = document.getElementById('message');

    function onChange(e) {
        if (editable.innerText.length != 0) {
            editable.innerHTML = editable.innerText;
        }
    }

    editable.addEventListener('paste', onChange, false);

    $('.media').hover(
        function() {
            $(this).css('background', 'lightgrey');
        },
        function() {
            $(this).css('background', 'white');
        }
    );
});