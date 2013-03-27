$(document).ready(function() {
$(".wait").hide();
$("#success-message").hide();

var defaultColor = $("input[name=name]").css('border-top-color');

$("form#contact").submit(function(e) {
    $("input[name=name]").css('border-color',defaultColor);
    $("input[name=email]").css('border-color',defaultColor);
    $("input[name=subject]").css('border-color',defaultColor);
    $("input[name=captcha]").css('border-color',defaultColor);
    $("textarea[name=message]").css('border-color',defaultColor);

    e.preventDefault();
    var name = $.trim($("input[name=name]").val()),
        email = $.trim($("input[name=email]").val()),
        subject = $.trim($("input[name=subject]").val()),
        captcha = $.trim($("input[name=captcha]").val()),
        message = $.trim($("textarea[name=message]").val()),
        succeed = false, error=false;
    
    if (name.length == 0)  {
        $("input[name=name]").css('border-color', 'red');
        error = true;
    }
    
    if (email.length == 0) {
        $("input[name=email]").css('border-color', 'red');
        error = true;
    }
    
    if (subject.length == 0) {
        $("input[name=subject]").css('border-color', 'red');
        error = true;
    }
    
    if (message.length == 0) {
        $("textarea[name=message]").css('border-color', 'red');
        error = true;
    }
    
    if (captcha.length == 0)  {
        $("input[name=captcha]").css('border-color', 'red');
    }
    if (error) {
        return;
    }
    
    $(this).slideUp(function() { $(".wait").show() });
    $.post('/plugins/contact/send/', { name: name, email: email, subject: subject, message: message, captcha:captcha })
        .complete(function() { $(".wait").hide(); })
        .success(function(data) {
            if (data.error.length == 0) {
                $("#success-message").show();
                $("form#contact").remove();
            } else {
                for (err in data.error) {
                    if (err == 'name') {
                        $("input[name=name]").css('border-color', 'red');
                    } else if (err = 'email') {
                        $("input[name=email]").css('border-color', 'red');
                    } else if (err == 'subject') {
                        $("input[name=subject]").css('border-color', 'red');
                    } else if (err == 'message') {
                        $("textarea[name=message]").css('border-color', 'red');                                    
                    } else if (err == 'captcha') {
                        $("input[name=captcha]").css('border-color', 'red');                                    
                    }
                }
                $("form#contact").slideDown();
            }
        })
        .error(function() {
            alert("Unable to send the message to the server.");
            $(this).slideDown();
        });
});
});
