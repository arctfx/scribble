        var can_draw = false
        var can_chat = true

        const roomName = JSON.parse(document.getElementById('room-name').textContent);
        document.querySelector('#room-id').innerHTML += roomName;
        const userName = JSON.parse(document.getElementById('user-name').textContent);
        document.querySelector('#user-id').innerHTML += userName;

        //Update player
        /*$.ajax({
            type: 'POST',
            url: "update_player/",
            data: { "nickname": userName, "online": true },
            success: function (response) {
                console.log("Successfully updated player's status!"); //debug
            }
        });*/


        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

        const leaderboardSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/leaderboard/'
            + roomName
            + '/'
        );

        const gameSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/game/'
            + roomName
            + '/'
        );

        //Player list
        var playerList = document.getElementById("player-list");
        leaderboardSocket.onopen = function(e) {
            leaderboardSocket.send("Player connected");
            $.ajax({
                type: 'POST',
                url: "update_player/",
                data: { "nickname": userName, "online": true },
                success: function (response) {
                    console.log("Successfully updated player's status!"); //debug
                }
            });
        };


        leaderboardSocket.onmessage = function(e) {
            //console.log("Received message from leaderboardSocket: " + e.data)
            const data = JSON.parse(e.data);
            console.log(data);

            playerList.innerHTML = "";
            Object.keys(data).forEach( playerName => {
                var player = data[playerName];

                var entry = document.createElement('li');
                entry.style.cssText = player.online ? "color: #cccccc;" : "color: #777777;";
                entry.appendChild(document.createTextNode(
                    playerName + " - " + player.score
                ));
                playerList.appendChild(entry);
            });

            // TBR
            /*try {
                $.ajax({
                    type: 'GET',
                    url: "get_players/",
                    data: { "room_name": roomName },
                    datatype: 'json',
                    success: function(response) {
                        response.forEach( element => {
                            var entry = document.createElement('li');
                            entry.style.cssText = element.online ? "color: #cccccc;" : "color: #777777;";
                            entry.appendChild(document.createTextNode(
                                element.nickname + " - " + (element.online ? "online" : "offline")
                            ));
                            playerList.appendChild(entry);
                        });
                    }
                });
            }
            catch(err) {
                console.log(err.message);
            }*/
        };


        chatSocket.onmessage = function(e) {
            try {
                const data = JSON.parse(e.data);
                console.log(e.data); //debug
                console.log(data.type); //debug

                e.preventDefault();

                $.ajax({
                    type: 'POST',
                    url: "send_message/",
                    data: {
                            sender: data.sender,
                            text: data.message
                          },
                    success: function (response) {
                        console.log("Successfully received message!");
                    }
                });

                textarea = document.querySelector('#chat-log');
                if (data.sender === null) {
                    textarea.value += (data.message + '\n');
                }
                else {
                    textarea.value += (data.sender + ": " + data.message + '\n');
                }
                textarea.scrollTop = textarea.scrollHeight;
                console.log(data.sender); // debug
            } catch(err) {
                console.log("Invalid data received from WebSocket: {err.message}");
            }
        };


        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        leaderboardSocket.onclose = function(e) {
            console.error('Leaderboard socket closed unexpectedly');
        };


        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };


        document.querySelector('#chat-message-submit').onclick = function(e) {
            if (can_chat == true) {
                const messageInputDom = document.querySelector('#chat-message-input');
                const message = messageInputDom.value;
                messageInputDom.value = '';

                try {
                    $.ajax({
                        type: 'GET',
                        url: "guess_word/",
                        data: { "room_name": roomName, "user_name": userName, "word": message},
                        datatype: 'json',
                        success: function(response) {
                            console.log(response)
                            if (response.guessed == true) {
                                can_chat = false;
                                var msg = {
                                    "sender": null,
                                    "message": userName + " guessed the word!",
                                }
                                leaderboardSocket.send("Player connected");
                                chatSocket.send(JSON.stringify(msg));
                            }
                            else {
                                var msg = {
			                        "message": message,
			                        "sender": userName
			                    };
                                chatSocket.send(JSON.stringify(msg));
                            }
                        }
                    });
                }
                catch(err) {
                    console.log(err.message);
                }
            }
        };
