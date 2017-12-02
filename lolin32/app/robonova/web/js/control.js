jQuery(document).ready(function() {
    console.log(' document ready');

    jQuery('#sync').on('click', function(e)  {
        var now = new Date();
        var sendTime = {
          hour: now.getHours(),
          minute:now.getMinutes(),
          second:now.getSeconds()
        }
        t = JSON.stringify(sendTime)
        console.log('Sync clicked pc time: %s'%t);
        $.post('/time/set',t )
    });
    jQuery('#gettime').on('click', function(e)  {
        console.log('gettime clicked ');
        askTime();
    });

    function setPixel(){
        console.log('set pixel');
         i = $('#input_I').val(); 
         r = $('#input_R').val(); 
         g = $('#input_G').val();
         b = $('#input_B').val();
         if (mod ==="pixel")
            $.get("mode/pixel",{i:i,r:r,g:g,b:b});
         if (mod ==="color")
            $.get("mode/color",{r:r,g:g,b:b});
    }

    jQuery('#input_R').on('change', function(e)  {
        setPixel();
    });
    jQuery('#input_G').on('change', function(e)  {
        setPixel();
    });
    jQuery('#input_B').on('change', function(e)  {
        setPixel();
    });
    jQuery('#input_I').on('change', function(e)  {
        setPixel();
    });

    function setOffset(delta){
        console.log('set offset');
        offset +=delta;
        offset %=60;
        if (offset < 0)
            offset = 60 - offset;
        var value = { pos: offset }
        $.post('/settings/offset',JSON.stringify(value) )
    }


    jQuery('#input_brightness').on('change', function(e)  {
        var value = { v: $('#input_brightness').val() }
        $.post('/settings/brightness',JSON.stringify(value) )
    });
    jQuery('#m10').on('click', function(e)  {
        setOffset(-10)
    });
    jQuery('#m1').on('click', function(e)  {
        setOffset(-1)
    });
    jQuery('#p1').on('click', function(e)  {
        setOffset(1)
    });
    jQuery('#p10').on('click', function(e)  {
        setOffset(10)
    });

    jQuery('#input_quarters').on('change', function(e)  {
        var value = { v: $('#input_quarters').val() }
        $.post('/settings/quarters',JSON.stringify(value) )
    });
    jQuery('#mode_pixel').on('click', function(e)  {
        mod  = "pixel";
        console.log('mode pixel clicked ');
        setPixel()
    });
    jQuery('#mode_color').on('click', function(e)  {
        console.log('mode color clicked ');
        mod  = "color";
         i = $('#input_I').val(); 
         r = $('#input_R').val(); 
         g = $('#input_G').val();
         b = $('#input_B').val();
        $.get("mode/color",{r:r,g:g,b:b});
    });
    jQuery('#mode_klok').on('click', function(e)  {
        console.log('mode klok clicked ');
        mod  = "klok";
        $.get("mode/klok");
    });
    jQuery('#mode_rainbow').on('click', function(e)  {
        console.log('mode rainbow clicked ');
        $.get("mode/rainbow");
    });



    jQuery('.slider_pos').on('change', function(e)  {
        var value = { id:$(this).attr('id') , group:$(this).attr('group') , pos: $(this).val() }
        $.post('/servos/position',JSON.stringify(value) )
    });

    jQuery('.slider_posall').on('change', function(e)  {
        var value = { group:$(this).attr('group') , pos: $(this).val() }
        $.post('/servos/all',JSON.stringify(value) )
    });

    jQuery('#button_servoIdL').on('click', function(e)  {
        newId = $('#input_servoIdL').val()
        console.log('setId for left group newId:', newId);
        var value = { id: newId, group:"L" }
        $.post('/servos/id',JSON.stringify(value) )
    });
    jQuery('#button_servoIdR').on('click', function(e)  {
        newId = $('#input_servoIdR').val()
        console.log('setId for left group newId:', newId);
        var value = { id: newId, group:"R" }
        $.post('/servos/id',JSON.stringify(value) )
    });
    jQuery('.button_off').on('click', function(e)  {
        var value = { onoff:'0', group:$(this).attr('group') }
        console.log('motors off for group :', value);
        $.post('/servos/off',JSON.stringify(value) )
    });
    jQuery('.button_on').on('click', function(e)  {
        var value = { onoff:'1', group:$(this).attr('group') }
        console.log('motors on for group :', value);
        $.post('/servos/off',JSON.stringify(value) )
    });
    jQuery('.button_exit').on('click', function(e)  {
        var value = { onoff:'-1', group:$(this).attr('group') }
        console.log('motors exit for group :', value);
        $.post('/servos/off',JSON.stringify(value) )
    });


    var getPositionL = function () {
        $.ajax({
            url: '/servos/positions?group=L',
            success: function(data, status, xhdr)
                    {
                        for (i = 0; i < 9; i++) { 
                            var s = '.left #' + i + '.label_pos'; 
                            jQuery(s).text ( data[i] );
                            //s = '.left #' + i + '.slider_pos.left'
                            //jQuery(s).val  ( data[i] );
                        }
                    },
            dataType: 'json'
        }).fail( function(xhr, status, error) {
            console.log("An AJAX error occured: " + status + "\nError: " + error + "\nError detail: " + xhr.responseText);
        });
    }
    var getPositionR = function () {
        $.ajax({
            url: '/servos/positions?group=R',
            success: function(data, status, xhdr)
                    {
                        for (i = 0; i < 9; i++) { 
                            var s = '.right #' + i + '.label_pos'; 
                            jQuery(s).text ( data[i] );
                            //s = '.right #' + i + '.slider_pos'
                            //jQuery(s).val  ( data[i] );
                        }
                    },
            dataType: 'json'
        }).fail( function(xhr, status, error) {
            console.log("An AJAX error occured: " + status + "\nError: " + error + "\nError detail: " + xhr.responseText);
        });
    }
    var t = setInterval(getPositionL,500);
    var u = setInterval(getPositionR,500);

});