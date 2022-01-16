$(document).ready(function (e) {
    var socket = io.connect('http://localhost:5000');
    console.log("Connected");

    $('input.sync').on('input', function (event) {
        socket.emit('data value changed', {
            which: document.getElementById('title'),
            who: $(this).attr('id'),
            data: $(this).val()
        });
        return false;
    });


});