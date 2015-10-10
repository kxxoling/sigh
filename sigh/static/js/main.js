$().ready(function () {

  $("form#new .tags.select2").select2({
    tags: true
  });

  $("form#new").on("submit", function(event){
    event.preventDefault();
    var $form = $(this);
    $.ajax({
      type: $form.attr("method"),
      url: $form.attr("action"),
      data: $form.serialize(),
      success: function(e, status) {
        if (e.redirect_url){
          window.location.href = e.redirect_url;
        }
      },
      error: function(e, status) {
        var errors = e.responseJSON;
        $form.find(".content").addClass("has-error").find("span.tip").text(errors.content[0])
      }
    });
  });

  /*
    Clear error tip when input or textarea element is clicked.
   */
  $("form input.form-control, form textarea.form-control").on("click", function(){
    var self = $(this);
    self.parents(".has-error.form-group").removeClass("has-error");
    self.siblings("span.tip").text("");
  });

  $("select.select2.tags").select2({
    ajax: {
      delay: 500,
      url: function(params){
        return '/api/tag/autocompletion/' + params.term
      },
      processResults: function (oriData) {
        var data = [];
        oriData.forEach(function(d){
          data.push({
            id: d['id_'],
            text: d['display_name']
          })
        });
        return {results: data}
      },
      cache: "true"
    }
  });

});
