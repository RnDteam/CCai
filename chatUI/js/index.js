    // Encoding and Decoding server's data
    function encode_utf8(s) {
      return unescape(encodeURIComponent(s));
    }

    function decode_utf8(s) {
      return decodeURIComponent(escape(s));
    }


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
    }

    function msgEvt(message) {
       // Decoding and replacing \n by br
        message = message.split('\n');
        message = message.join("<br/>");
        scrollDown()
    }

    num=0


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

        var list = xmlDoc.getElementsByTagName("button");
        for (i=0; i< list.length; i++){
            b = xmlDoc.createElement("button");
            b.type = "button"
            b.className ="btn"
            b.id = "btn" + num
            b.innerHTML = list[i].innerHTML
            b.setAttribute("background-color","#476e9e");
            b.setAttribute("onclick", "clickBtn(this)");
            b.setAttribute("value",  list[i].innerHTML);
            b.setAttribute("onmouseover", "hover(this)")
            xmlDoc.documentElement.replaceChild(b, list[i]);
            num += 1
        }
        message = xmlDoc.getElementsByTagName("text")[0];

        addMsg('ccai.jpg',message.innerHTML)
        //msgEvt(message)
    }

    function clickBtn(btn){
        addMsg('tsvika.jpg',btn.value)
        websocket.send(btn.value)
        for(i=0; i<num;i++){
            document.getElementById("btn"+i).disabled=true;
            document.getElementById("btn"+i).setAttribute("background-color","#44668f");
        }
        scrollDown()
    }
    function scrollDown(){
        var objDiv = document.getElementById("list-chat");
        objDiv.scrollTop = objDiv.scrollHeight;
    }

    $('.mdi-send').on('click', function() {
        if($('.chat-input').val().length > 0) {
            addMsg('tsvika.jpg',$('.chat-input').val());
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


