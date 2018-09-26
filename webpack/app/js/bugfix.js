export default class BugFix {
  constructor(tile) {
    this.bugfixBase();
    this.bugfixQuerywidget();
  }
  /*
   * Bug fix para o bug de <base url=""> do Plone
   */
  bugfixBase() {
    if($("base").length > 0 && $(".userrole-anonymous").length > 0) {
      var aCurrentUrl = document.location.href.match(/(^[^#]*)/);
      $("base").attr("href", aCurrentUrl[1]);
    }
  }
  /*
   * Bug fix para o bug de plone.formwidget.querystring versao acima de 1.0b3
   */
  bugfixQuerywidget() {
    if ($(".QueryWidget").length === 0) {
      return false;
    }
    $.querywidget.init();
    $('#sort_on').val($('#form-widgets-sort_on').val());
    if ($('#form-widgets-sort_reversed-0').attr('checked')) {
      $('#sort_order').attr('checked', true);
    } else {
      $('#sort_order').attr('checked', false);
    }
    $("#sort_on").live('click', function () {
      $('#form-widgets-sort_on').val($(this).val());
    });
    $("#sort_order").live('click', function () {
      if ($(this).is(":checked")) {
        $('#form-widgets-sort_reversed-0').attr('checked', true);
      } else {
        $('#form-widgets-sort_reversed-0').attr('checked', false);
      }
    });
    $('#formfield-form-widgets-sort_on').hide();
    $('#formfield-form-widgets-sort_reversed').hide();
  }
}
