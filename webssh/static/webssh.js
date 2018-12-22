function get_connect_argv() {
    var host = $('#host').val();
    var port = $('#port').val();
    var user = $('#user').val();
    var auth = $("input[name='inlineRadioOptions']:checked").val();
    var pwd = $('#password').val();
    var password = window.btoa(pwd);
    var pkey = $('#pkey').val();

    var argv = 'host=' + host + '&port=' + port + '&user=' + user + '&auth=' + auth + '&password=' + password + '&pkey=' + pkey;
    return argv
}


function webssh() {
    var argv = get_connect_argv();

    terminado.apply(Terminal);
    var term = new Terminal(
        {
            cols: 200,
            rows: 50,
            useStyle: true,
            cursorBlink: true
        }
    ),
        protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://',
        socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') +
            '/webssh/?' + argv;

    var sock = new WebSocket(socketURL);

    sock.addEventListener('open', function () {
        $('#form').addClass('hide');
        $('#django-webssh-terminal').removeClass('hide');

        term.terminadoAttach(sock);
    });

    sock.addEventListener('message', function (recv) {
        var content = JSON.parse(recv.data.toString());
        term.write(content)
    });

    term.on('data', function (data) {
        var send_data = JSON.stringify({'data': data});
        sock.send(send_data)
    });

    term.open(document.getElementById('terminal'));
}
