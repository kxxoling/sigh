$().ready(function () {

  $("form.comment").on("submit", function (event) {
    event.preventDefault();
    var $form = $(this);
    var $comments = $(".comment-group");
    $.ajax({
      type: $form.attr("method"),
      url: $form.attr("action"),
      data: $form.serialize(),
      success: function (e, status) {
        $comments.prepend("<p>"+e.content+"</p>");
      },
      error: function (e, status) {
        var errors = e.responseJSON;
        $form.find(".content").addClass("has-error").find("span.tip").text(errors.content[0])
      }
    });
    return false;
  });

});