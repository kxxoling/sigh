$().ready(function () {

  $("form.comment").on("submit", function (event) {
    event.preventDefault();
    var $form = $(this);
    var $commentTableFirstColumn = $(".comment.list .list-item:first");
    var $input = $("textarea.comment");
    $.post($form.attr("action"), $form.serialize(), function (data, status) {
        var $user = $('.comment-form .avatar')
        var image = $user.data('avatar'),
            username = $user.data('username'),
            fullname = $user.data('name'),
            id=$user.data('id'),
            content = data.content;

        var rowStr = '<div class="list-item">\
<div class="list-left">\
<div style="background-image: url('+ image +')" class="avatar"></div>\
</div>\
<div class="list-right">\
<div class="relate-info clearfix">\
<div class="pull-left"><a data-username="' + username + '" href="/u/+ id +/" class="name">' + fullname +'</a>\
</div>\
<div class="pull-right"><span class="time">' + 'Just now' + '</span>\
</div>\
</div>\
<div class="content"><p>'+ content + '</p></div>\
</div>\
</div>'
        $commentTableFirstColumn.before(rowStr);
        $input.val("");
      }, 'json').fail(function (e, status) {
        var errors = e.responseJSON;
        console.log(errors);
        $form.addClass("has-error");
        setTimeout(function () {
          $form.removeClass('has-error')
        }, 2000);
      });
    return false;
  });

});
