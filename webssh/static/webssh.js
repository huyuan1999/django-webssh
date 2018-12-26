function post_data() {
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var host = $('#host').val();
    var port = $('#port').val();
    var user = $('#user').val();
    var auth = $("input[name='auth']:checked").val();
    var pwd = $('#password').val();
    var password = window.btoa(pwd);

    var data = {
        'host': host,
        'port': port,
        'user': user,
        'auth': auth,
        'password': password,
    };

    var unique = null;

    if (auth === 'key') {
        var pkey = $('#pkey')[0].files[0];
        var formData = new FormData();
        formData.append('pkey', pkey);
        formData.append('data', JSON.stringify(data));
        formData.append('csrfmiddlewaretoken', csrf);

        $.ajax({
            url: "/",
            type: "post",
            data: formData,
            async: false,
            contentType: false,
            processData: false,
            mimeType: 'multipart/form-data',
            success: function (result) {
                var obj = JSON.parse(result);
                var code = obj.code;
                if (code === 0) {
                    unique = obj.message;
                } else {
                    var error = obj.error;
                    try {
                        var error_obj = JSON.parse(error);
                        Object.keys(error_obj).forEach(function (key) {
                            var error_info = 'field: ' + key + ' ' + error_obj[key][0].message;
                            $('#' + key).after(' ' + '<span style="color: red">' + error_info + '</span>');
                        })
                    } catch (e) {
                        alert(error);
                    }
                }
            }
        })
    } else {
        $.ajax({
            url: "/",
            type: "post",
            data: {'data': JSON.stringify(data), 'csrfmiddlewaretoken': csrf},
            async: false,
            success: function (result) {
                var obj = result;
                var code = obj.code;
                if (code === 0) {
                    unique = obj.message;
                } else {
                    var error = obj.error;
                    try {
                        var error_obj = JSON.parse(error);
                        Object.keys(error_obj).forEach(function (key) {
                            var error_info = 'field: ' + key + ' ' + error_obj[key][0].message;
                            $('#' + key).after(' ' + '<span style="color: red">' + error_info + '</span>');
                        })
                    } catch (e) {
                        alert(error);
                    }
                }
            }
        })
    }

    if (unique !== null) {
        webssh(unique)
    }
}


function get_term_size() {
    var init_width = 9;
    var init_height = 17;

    var windows_width = $(window).width();
    var windows_height = $(window).height();
    console.log(windows_width, windows_height);
    return {
        cols: Math.floor(windows_width / init_width),
        rows: Math.floor(windows_height / init_height),
    }
}


function webssh(unique) {
    var cols = get_term_size().cols;
    var rows = get_term_size().rows;

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
            '/webssh/?'+ 'unique=' + unique + '&width=' + cols + '&height=' + rows;

    var sock = new WebSocket(socketURL);

    sock.addEventListener('open', function () {
        $('#form').addClass('hide');
        $('#django-webssh-terminal').removeClass('hide');
        term.open(document.getElementById('terminal'));
    });

    sock.addEventListener('message', function (recv) {
        var content = JSON.parse(recv.data.toString());
        term.write(content)
    });

    term.on('data', function (data) {
        var send_data = JSON.stringify({'data': data});
        sock.send(send_data)
    });


}
