$(document).ready(function() {
    $("#get-next").click(function() {
        $("div.wait").show();
        $.get('/blog/ajax/getnext/', {articles:$(".post").length}, function(data) {
            if (data.length == 0)
                $("#get-next").hide();
            else
                $(data).insertBefore($("div.wait")).hide().slideDown("slow");
            $("div.wait").hide();
        });
    });
    $("pre").addClass('highlight');
    $.SyntaxHighlighter.init();

});