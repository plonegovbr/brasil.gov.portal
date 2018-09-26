export default class SearchSuggestions {
  constructor() {
    $('#portal-searchbox .searchField').on('focus', (e) => {
      e.preventDefault();
      if ($('#search-overlay').length === 0) {
        $('#portal-searchbox > form').append('<div id="search-overlay"></div>');
      }
      $('#search-overlay').show();
      $('#portal-searchbox .search-suggestions').css('display', 'block');
    });

    $(document).on('click', '#search-overlay',  (e) => {
      e.preventDefault();
      $('#search-overlay').hide();
      $('#portal-searchbox .search-suggestions').hide();
    });
  }
}
