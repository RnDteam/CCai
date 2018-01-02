    // Encoding and Decoding server's data
    function encode_utf8(s) {
      return unescape(encodeURIComponent(s));
    }

    function decode_utf8(s) {
      return decodeURIComponent(escape(s));
    }
        user = "images/user.png"
        bot = "images/bot.png"

        document.getElementById("unit").src = "images/unit.png"
        document.getElementById("title").textContent = "combot"

    $('.list-chat').addClass('shown');
    $('.mdi-arrow-left').show();
    $('#content').addClass('chat');

    websocket = new WebSocket("ws://localhost:8000/");
    last = "";
    function addMsg(name,text){
        if (last == name)
            $('p:last').append('<p>' + text+ '</p>');
        else
            $('div.list-chat > ul').append('<li><img src="'+name+'""><div class="message"><p>' + text + '</p></div></li>');
        last = name

        scrollDown()
    }

    function msgEvt(message) {
       // Decoding and replacing \n by br
        message = message.split('\n');
        message = message.join("<br/>");
        scrollDown()
    }

    num=0
    num_disabled = 0

    websocket.onmessage = function (event) {
        var text = decode_utf8(event.data);
        var parser, xmlDoc;

        if (window.DOMParser) {
          parser = new DOMParser();
          xmlDoc = parser.parseFromString(text,"text/xml");
        } else {
          xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
          xmlDoc.async = false;
          xmlDoc.loadXML(text);
        }
        createButtons(xmlDoc);
        xmlDoc = createImages(xmlDoc)
        message = xmlDoc.getElementsByTagName("text")[0];

        addMsg(bot,message.innerHTML)

        scrollDown()
    }
    function createImages(xmlDoc){
        element = "image"
        var list = xmlDoc.getElementsByTagName(element);
        for (i=0; i< list.length; i++){
            var img = xmlDoc.createElement("IMG");
            img.setAttribute("src", "images/"+list[i].textContent);
            img.id = 1
            xmlDoc.documentElement.replaceChild(img, list[i]);
        }
        return xmlDoc
    }
    function createButtons(xmlDoc){
        btn = "button"
        var list = xmlDoc.getElementsByTagName(btn);
        for (i=0; i< list.length; i++){
            b = xmlDoc.createElement(btn);
            b.type = btn
            b.className = btn
            b.id = btn + num
            b.innerHTML = list[i].innerHTML
            b.setAttribute("onclick", "clickBtn(this)");
            b.setAttribute("value",  list[i].innerHTML);
            xmlDoc.documentElement.replaceChild(b, list[i]);
            num += 1
        }
    }

    function clickBtn(btn){
        addMsg(user,btn.value)
        websocket.send(btn.value)
        for(i=num_disabled; i<num;i++){
            document.getElementById("button"+i).disabled=true;
            document.getElementById("button"+i).className = "button disabled";
        }
        num_disabled = num;
        scrollDown()
    }
    function clickReset(btn){
        $('div.list-chat > ul').empty();
        last = "user"
        websocket.send(btn.title)
    }
    function clickBack(back){
        addMsg(user,back.title)
        websocket.send(back.title)
        scrollDown()
    }
    function scrollDown(){
        var objDiv = document.getElementById("list-chat");
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    $('.mdi-send').on('click', function() {
        if($('.chat-input').val().length > 0) {
            addMsg(user,$('.chat-input').val());
            websocket.send($('.chat-input').val())
            $('.chat-input').val('');
            scrollDown()
        }
    });

    //check for enter to send message
    $('.chat-input').on('keyup', function(event) {
        event.preventDefault();
        //enter
        if (event.which === 13) {
            $('.mdi-send').trigger('click');
        }


    });

    //full screen button
    $('#head').on('click', '.mdi-fullscreen', function() {
        $(this).removeClass('mdi-fullscreen').addClass('mdi-fullscreen-exit');
        $('#hangout').css({
            width: '900px'
        });
    });

    //full screen button - exit
    $('#head').on('click', '.mdi-fullscreen-exit', function() {
        $(this).removeClass('mdi-fullscreen-exit').addClass('mdi-fullscreen');
        $('#hangout').css({
            width: '400px'
        });
    });


