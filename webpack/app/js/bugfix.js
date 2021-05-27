export default class BugFix {
  constructor(tile) {
    this.bugfixBase();
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
}
