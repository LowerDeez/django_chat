// ------------------------------------------------------------------- //
// ------------------------------------------------------------------- //


function chat_rooms(id) {
    $.ajax({
        async: true,
        crossDomain: true,
        url: "/chat_rooms/" + id + "/",
        method: "GET",
        success: function(content) {
            $("#contacts").empty();
            $("#contacts").html(content);
        }
    });
}


$(document).ready(function() {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/chat/stream/";
    var socket = new ReconnectingWebSocket(ws_path);

    socket.onmessage = function (message) {
        var data = JSON.parse(message.data);
        var user_id = $('#user_id').attr('data-user-id');

        if (data.error) {
            alert(data.error);
            return;
        }
        if (data.join) {
            $('#chat_content').addClass('load');
            $.ajax({
                async: true,
                crossDomain: true,
                url: "/chats/get_messages/" + data.join + "/",
                method: "GET",
                success: function(content) {
                    $("#chat_content").html(content);
                    $(".messages").animate({scrollTop: $(".messages_room").height()}, "fast");
                    $("#send_message").on("click", function () {
                        if ($("#text_message").val() != '' && $("#text_message").val() != undefined) {
                            $('.messages_empty').remove();
                            socket.send(JSON.stringify({
                                "command": "send",
                                "room": data.join,
                                "message": $("#text_message").val()
                            }));
                            $("#text_message").val("");
                            return false;
                        }
                    });
                    $('#chat_content').removeClass('load');
                }
            });
        }
        else if (data.leave) {
            console.log("Leaving room " + data.leave);
            $("#room-" + data.leave).remove();
        }
        else if (data.message || data.msg_type != 0) {
            var room_id = "#messages_room_" + data.room;
            var msgdiv = $(room_id);
            var ok_msg = "";
            switch (data.msg_type) {
                case 0:
                    if (user_id == data.user_id) {
                        ok_msg = "<li class=\"replies\">" +
                                "<img src=\"" + data.user_avatar + "\" class=\"online\" alt=\"\"/>" +
                                "<span class='right'>" +
                                "<span class=\"strong\">" + data.username + "</span>&nbsp;" +
                                data.timestamp +
                                "</span><br>" +
                                "<p>" + data.message + "</p>" +
                                "</li>";
                    }
                    else {
                        ok_msg = "<li class=\"sent\">" +
                                "<img src=\"" + data.user_avatar + "\" class=\"online\" alt=\"\"/>" +
                                "<span>" +
                                "<span class=\"strong\">" + data.username + "</span>&nbsp;" +
                                data.timestamp +
                                "</span><br>" +
                                "<p>" + data.message + "</p>" +
                                "</li>";
                    }
                    chat_rooms(data.room);
                    break;
                case 1:
                    ok_msg = "<li class=\"sent\"><p>" + data.message + "<p></li>";
                    break;
                case 2:
                    ok_msg = "<li class=\"sent\"><p>" + data.message + "<p></li>";
                    break;
                case 3:
                    ok_msg = "<li class=\"sent\"><p>" + data.message + "<p></li>";
                    break;
                default:
                    return;
            }
            msgdiv.append(ok_msg);
            $(".messages").animate({scrollTop: $(".messages_room").height()}, "slow");
        }
        else {
            console.log("Cannot handle message!");
        }
    };

    $(document).on('click','li.room-link', function() {
        var room_id = $(this).attr("data-room-id");
        $('.contact').removeClass("active");
        $(this).addClass("joined");
        $(this).addClass("active");

        socket.send(JSON.stringify({
            "command": "join",
            "room": room_id
        }));
    });

    $(document).on('click','#sign_out_button', function() {
        window.location = '/logout/';
        return false;
    });

    socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };

    $(window).on('keydown', function (e) {
        if (e.which == 13) {
            if ($("#text_message").val() != '' && $("#text_message").val() != undefined) {
                var room_id = $('.messages_room').attr('data-room-id');
                $('.messages_empty').remove();
                socket.send(JSON.stringify({
                    "command": "send",
                    "room": room_id,
                    "message": $("#text_message").val()
                }));
                $("#text_message").val("");
                return false;
            }
        }
    });

    $(document).on('click','#profile-img', function() {
        var id = $(this).attr('data-id');
        window.location = '/user/' + id + '/';
        return false;
    });

    $(document).on('click','#btn_profile', function() {
        var id = $(this).attr('data-id');
        window.location = '/user/' + id + '/';
        return false;
    });

    $(document).on('click','#add_user', function() {
        window.location = 'chats/new/1/';
        return false;
    });

    $(document).on('click','#add_chat', function() {
        window.location = 'chats/new/2/';
        return false;
    });
});

