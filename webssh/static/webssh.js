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

function get_term_size() {
    var init_width = 8.9;
    var init_height = 16.5;

    var windows_width = $(window).width();
    var windows_height = $(window).height();

    return {
        cols: Math.floor(windows_width / init_width),
        rows: Math.floor( windows_height / init_height),
    }
}


function webssh() {
    var argv = get_connect_argv();
    var cols = get_term_size().cols;
    var rows = get_term_size().rows;

    terminado.apply(Terminal);
    var term = new Terminal(
        {
            cols: cols,
            rows: rows,
            useStyle: true,
            cursorBlink: true
        }
        ),
        protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://',
        socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') +
            '/webssh/?' + argv + '&width=' + cols + '&height=' + rows;

    console.log(socketURL);
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
