const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  // name
  'brasil.gov.portal',

  // shortName
  'brasilgovportal',

  // path
  `${__dirname}/../src/brasil/gov/portal/browser/viewlets/static`,

  //publicPath
  '++resource++brasil.gov.portal/',

  //callback
  function(config, options) {
    config.entry.unshift(
      './app/img/preview.png',
    );
  },
);
