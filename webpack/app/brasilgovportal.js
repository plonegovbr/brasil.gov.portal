import BugFix from './js/bugfix.js';
import SearchSuggestions from './js/search_suggestions.js';


// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(() => {
  new BugFix();
  new SearchSuggestions();
});


export default {
  BugFix,
  SearchSuggestions,
}
