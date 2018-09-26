module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['mocha', 'chai', 'sinon'],
    files: [
      './tests/*.spec.js'
    ],
    exclude: [],
    preprocessors: {
      './tests/*.spec.js': ['webpack']
    },
    // webpack configuration
    webpack: require("./webpack.config.js"),
    webpackMiddleware: {
      stats: "errors-only"
    },
    reporters: ['progress'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['Chrome'],
    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exists
    singleRun: false,
    concurrency: Infinity
  })
}
