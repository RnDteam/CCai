    // Encoding and Decoding server's data
    function encode_utf8(s) {
      return unescape(encodeURIComponent(s));
    }

    function decode_utf8(s) {
      return decodeURIComponent(escape(s));
    }

    // First route to show
    var GLOBALSTATE = {
        route: '.list-chat'
    };

    // Set first Route
    setRoute(GLOBALSTATE.route);
    $('.nav > li[data-route="' + GLOBALSTATE.route + '"]').addClass('active');

    //dirtiest, ugliest, hackiest ripple effect solution ever... but they work xD
    $('.floater').on('click', function(event) {
        var $ripple = $('<div class="ripple tiny bright"></div>');
        var x = event.offsetX;
        var y = event.offsetY;
        var $me = $(this);

        $ripple.css({
            top: y,
            left: x
        });
        $(this).append($ripple);

        setTimeout(function() {
            $me.find('.ripple').remove();
        }, 530)

    });

    // Have to Delegate ripple due to dom manipulation (add)
    $('ul.mat-ripple').on('click', 'li', function(event) {
        if ($(this).parent().hasClass('tiny')) {
            var $ripple = $('<div class="ripple tiny"></div>');
        } else {
            var $ripple = $('<div class="ripple"></div>');
        }
        var x = event.offsetX;
        var y = event.offsetY;

        var $me = $(this);

        $ripple.css({
            top: y,
            left: x
        });

        $(this).append($ripple);

        setTimeout(function() {
            $me.find('.ripple').remove();
        }, 530)
    });


    // Dyncolor ftw
    if (localStorage.getItem('color') !== null) {
        var colorarray = JSON.parse(localStorage.getItem('color'));
        stylechange(colorarray);
    } else {
        var colorarray = [15, 157, 88]; // 15 157 88 = #0f9d58
        localStorage.setItem('color', JSON.stringify(colorarray));
        stylechange(colorarray);
    }


    // Stylechanger
    function stylechange(arr) {
        var x = 'rgba(' + arr[0] + ',' + arr[1] + ',' + arr[2] + ',1)';
        $('#dynamic-styles').text('.dialog h3 {color: ' + x + '} .i-group input:focus ~ label,.i-group input.used ~ label {color: ' + x + ';} .bar:before,.bar:after {background:' + x + '} .i-group label {color: ' + x + ';} ul.nav > li.active {color:' + x + '} .style-tx {color: ' + x + ';}.style-bg {background:' + x + ';color: white;}@keyframes navgrow {100% {width: 100%;background-color: ' + x + ';}} ul.list li.context {background-color: ' + x + '}');
    }

    function closeModal() {
        $('#new-user').val('');
        $('.overlay').removeClass('add');
        $('.floater').removeClass('active');
        $('#contact-modal').fadeOut();

        $('#contact-modal').off('click', '.btn.save');

    }

    function setModal(mode, $ctx) {
        var $mod = $('#contact-modal');
        switch (mode) {
            case 'add':
                $mod.find('h3').text('Add Contact');
                break;

            case 'edit':
                $mod.find('h3').text('Edit Contact');
                $mod.find('#new-user').val($ctx.text()).addClass('used');
                break;
        }

        $mod.fadeIn();
        $('.overlay').addClass('add');
        $mod.find('#new-user').focus();
    }

    $('.mdi-arrow-left').on('click', function() {
        $('.shown').removeClass('shown');
        setRoute('.list-text');
    });

    // Set Routes - set floater
    function setRoute(route) {
        GLOBALSTATE.route = route;
        $(route).addClass('shown');

        if (route !== '.list-account') {
            $('#add-contact-floater').addClass('hidden');
        } else {
            $('#add-contact-floater').removeClass('hidden');
        }

        if (route !== '.list-text') {
            $('#chat-floater').addClass('hidden');
        } else {
            $('#chat-floater').removeClass('hidden');
        }

        if (route === '.list-chat') {
            $('.mdi-menu').hide();
            $('.mdi-arrow-left').show();
            $('#content').addClass('chat');
        } else {
            $('#content').removeClass('chat');
            $('.mdi-menu').show();
            $('.mdi-arrow-left').hide();
        }
    }

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

        if (message.indexOf('[') > -1){
            var opt = (message).split('[');
            addMsg('ccai.jpg',opt[0]);
            $('p:last').append('<p></p>');
        }
        if (message.indexOf('[') > -1){
            var str = (message).split('[');
            var str2 = (str[1]).split(']');
            var opt = str2[0].split('|')
            name = 'ccai.jpg'
            for (i = 0; i < opt.length; i++) {
                id = "btn" +num
                text = '<button type="button" class="btn" id='+id+' value="'+opt[i]+'" onclick = "clickBtn(this)">'+opt[i]+'</button>'
                num+=1
                if (last == name)
                    $('p:last').append(text);
                else
                    $('div.list-chat > ul').append('<li><img src="'+name+'""><div class="message"><p>' + text + '</p></div></li>');
                last = name
            }
            $('p:last').append("<p>"+str2[1]+"</p>");
        } else
            addMsg('ccai.jpg',message)

        scrollDown()
    }

    function typingAnimation(time,typeText,msg){
        var dots = 0;
        var t0 = performance.now();
        addMsg('ccai.jpg',typeText);
        myvar = setInterval (type, 600);
        function type()
        {
            if(dots < 3)
            {
                $('p:last').append('.');
                dots++;
            }
            else
            {
                $('p:last').html(typeText);
                dots = 0;
            }
          if (performance.now()-t0>time){
            clearTimeout(myvar);
            $('p:last').html('');
            msgEvt(msg)
           }
            scrollDown()
        }
    }
    num=0
    websocket.onmessage = function (event) {
        message = decode_utf8(event.data);
        if (message.indexOf('{') != -1){
            var str = (message).split('{');
            var str2 = (str[1]).split('|');
            var str3 = str2[1].split('}')
            var str4 = (message).split('}')
            time = str2[0]
            typeText = str3[0]
            msg = str4[1]
            typingAnimation(time,typeText,msg);
        }else
            msgEvt(message)
    }

    function clickBtn(btn){
        addMsg('tsvika.jpg',btn.value)
        websocket.send(btn.value)
        for(i=0; i<num;i++)
            document.getElementById("btn"+i).disabled=true;
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

    $('.chat-input').on('keyup', function(event) {
        event.preventDefault();
        if (event.which === 13) {
            $('.mdi-send').trigger('click');
        }


    });

    $('.list-text > ul > li').on('click', function() {
        $('ul.chat > li').eq(1).html('<img src="' + $(this).find('img').prop('src') + '"><div class="message"><p dir="auto">' + $(this).find('.txt').text() + '</p></div>');

        // timeout just for eyecandy...
        setTimeout(function() {
            $('.shown').removeClass('shown');

            $('.list-chat').addClass('shown');
            setRoute('.list-chat');
            $('.chat-input').focus();
        }, 300);
    });

    // List context
    // Delegating for dom manipulated list elements
    $('.list-account > .list').on('click', 'li', function() {
        $(this).parent().children().removeClass('active');
        $(this).parent().find('.context').remove();
        $(this).addClass('active');
        var $TARGET = $(this);
        if (!$(this).next().hasClass('context')) {
            var $ctx = $('<li class="context"><i class="mdi mdi-pencil"></i><i class="mdi mdi-delete"></i></li>');

            $ctx.on('click', '.mdi-pencil', function() {
                setModal('edit', $TARGET);

                $('#contact-modal').one('click', '.btn.save', function() {
                    $TARGET.find('.name').text($('#new-user').val());
                    closeModal();
                });
            });

            $ctx.on('click', '.mdi-delete', function() {
                $TARGET.remove();
            });


            $(this).after($ctx);
        }
    });

    // Navigation
    $('.nav li').on('click', function() {
        $(this).parent().children().removeClass('active');
        $(this).addClass('active');
        $('.shown').removeClass('shown');
        var route = $(this).data('route');
        $(route).addClass('shown');
        setRoute(route);
    });

    $('#head').on('click', '.mdi-fullscreen', function() {
        $(this).removeClass('mdi-fullscreen').addClass('mdi-fullscreen-exit');
        $('#hangout').css({
            width: '900px'
        });
    });

    $('#head').on('click', '.mdi-fullscreen-exit', function() {
        $(this).removeClass('mdi-fullscreen-exit').addClass('mdi-fullscreen');
        $('#hangout').css({
            width: '400px'
        });
    });

    // menuclick
    $('#head .mdi-menu').on('click', function() {
        $('.menu').toggleClass('open');
        $('.overlay').toggleClass('add');
    });

    // viewtoggle > 1000
    $('#head .mdi-chevron-down').on('click', function() {
        if ($('#hangout').hasClass('collapsed')) {
            $(this).removeClass('mdi-chevron-up').addClass('mdi-chevron-down');
            $('#hangout').removeClass('collapsed');
        } else {
            $(this).removeClass('mdi-chevron-down').addClass('mdi-chevron-up');
            $('#hangout').addClass('collapsed');
        }

    });

    // Filter
    $('.search-filter').on('keyup', function() {
        var filter = $(this).val();
        $(GLOBALSTATE.route + ' .list > li').filter(function() {
            var regex = new RegExp(filter, 'ig');

            if (regex.test($(this).text())) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // killit
    $('#contact-modal').on('click', '.btn.cancel', function() {
        closeModal();
    });

    $('#new-user').on('keydown', function(event) {
        switch (event.which) {
            case 13:
                event.preventDefault();
                $('.btn.save').trigger('click');
                break;

            case 27:
                event.preventDefault();
                $('.btn.cancel').trigger('click');
                break;
        }

    });

    $('#add-contact-floater').on('click', function() {
        if ($(this).hasClass('active')) {
            	closeModal();
            $(this).removeClass('active');

        } else {

            $(this).addClass('active');
            setModal('add');
            $('#contact-modal').one('click', '.btn.save', function() {
                $('.list-account > .list').prepend('<li><img src="http://lorempixel.com/100/100/people/1/"><span class="name">' + $('#new-user').val() + '</span><i class="mdi mdi-menu-down"></i></li>');
                closeModal();
            });
        }
    });