var MILLS_TO_IGNORE_SEARCH = 100;

$(document).ready(function()  {
  /*
    Warning: Placing the true parameter outside of the debounce call:

    $('#color_search_text').keyup(_.debounce(processSearch,
        MILLS_TO_IGNORE_SEARCH), true);

    results in "TypeError: e.handler.apply is not a function"
   */
  $('#movie_search_text').keyup(_.debounce(processSearch, MILLS_TO_IGNORE_SEARCH,
      true));
});