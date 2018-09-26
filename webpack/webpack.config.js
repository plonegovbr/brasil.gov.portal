const childProcess = require('child_process');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');


const path = `${__dirname}/../src/brasil/gov/portal/browser/viewlets/static`;

// https://github.com/alleyinteractive/webpack-git-hash/issues/10
const gitCmd = 'git rev-list -1 HEAD -- `pwd`'
const gitHash = childProcess.execSync(gitCmd).toString().substring(0, 7);
childProcess.execSync(`rm -f ${path}/brasilgovportal-*`);


module.exports = {
  entry: [
    './app/brasilgovportal.scss',
    './app/brasilgovportal.js',
  ],
  output: {
    filename: `brasilgovportal-${gitHash}.js`,
    library: 'brasilgovportal',
    libraryExport: 'default',
    libraryTarget: 'umd',
    path: path,
    pathinfo: true,
    publicPath: '++resource++brasil.gov.portal/',
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.scss$/,
      use: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      }),
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            context: 'app/',
          }
        },
        {
          loader: 'image-webpack-loader',
          query: {
            mozjpeg: {
              progressive: true,
            },
            pngquant: {
              quality: '65-90',
              speed: 4,
            },
            gifsicle: {
              interlaced: false,
            },
            optipng: {
              optimizationLevel: 7,
            }
          }
        }
      ]
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      use: 'svg-url-loader',
    }]
  },
  plugins: [
    new ExtractTextPlugin({
      filename: `brasilgovportal-${gitHash}.css`,
      allChunks: true
    }),
    new HtmlWebpackPlugin({
      inject: false,
      filename: 'resources.pt',
      template: 'app/resources.pt',
    }),
    new SpritesmithPlugin({
      src: {
        cwd: 'app/sprite',
        glob: '*.png',
      },
      target: {
        image: 'app/img/sprite.png',
        css: 'app/scss/_sprite.scss',
      },
      apiOptions: {
        cssImageRef: './img/sprite.png',
      }
    }),
  ]
}
