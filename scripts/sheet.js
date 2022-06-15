$(document).ready(function (e) {
    var id = $('#title').attr('value')
    
    var jsonPath = './sheet' + id + '.json';

    var socket = io.connect('http://localhost:5000');
    console.log("Connected");
    socket.emit('join', {"id": id})
    $('#name').val('aa')

    function send_data(event) {

    }

    function get_data(event) {
        $.getJSON(jsonPath, function (new_data) { data = new_data });
        console.log(data['name'])
    }

    $('.sync').on('input', function (event) {
        socket.emit('data value changed', {
            id: id,
            field: $(this).attr('id'),
            value: $(this).val()
        });
        console.log("Message sent")
        return false;
    });


    socket.on('update', function(msg) {
        console.log(msg);
        console.log(msg['field'] + ', ' + msg['value'])
        $('#' + msg['field']).val(msg['value']);
    });
    
    socket.on('message', function(msg) {console.log(msg);});
    socket.on('exception', function(error) {console.error(error['errorMessage']);});
});