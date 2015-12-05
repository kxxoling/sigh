$().ready(function () {

  $("form.comment").on("submit", function (event) {
    event.preventDefault();
    var $form = $(this);
    var $commentTableFirstColumn = $("table.comment tr:first");
    var $input = $("textarea.comment");
    $.ajax({
      type: $form.attr("method"),
      url: $form.attr("action"),
      data: $form.serialize(),
      success: function (e, status) {
        var image = '',
            username = '',
            fullname = '',
            content = '';
        $row = '<tr>\
  <td class="left">\
    <div style="background-image: url("'
        + image + '")" class="avatar"></div>\
  </td>\
  <td class="right">\
    <div class="relate-info clearfix">\
      <div class="pull-left"><a data-username="'
        + username + '" href="/u/1/" class="name">'
        + fullname + '</a>\
      </div>\
      <div class="pull-right"><span class="time">Just now</span>\
      </div>\
    </div>\
    <div class="content">\
      <p>'
        + content + '</p>\
    </div>\
  </td>\
</tr>';
        $commentTableFirstColumn.before($row);
        $input.val("");
      },
      error: function (e, status) {
        var errors = e.responseJSON;
        $form.find(".content").addClass("has-error").find("span.tip").text(errors.content[0])
      }
    });
    return false;
  });

});
