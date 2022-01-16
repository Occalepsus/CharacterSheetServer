$(document).ready(function (e) {
    var socket = io.connect('http://localhost:5000');
    console.log("Connected");

    $('input.sync').on('input', function(event) {
        socket.emit('data value changed', {
            which: document.getElementById('title').val(),
            who: $(this).attr('id'),
            data: $(this).val()
        });
        return false;
    });

    socket.on('after connect', function(msg) {
        console.log('After connect', msg);
    });

    socket.on('update', function(msg) {
        console.log('value changed', msg);
        $('#'+msg.who).val(msg.data);
    });
});