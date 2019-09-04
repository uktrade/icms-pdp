var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    entry: [
      './web/static/web/js/entry',
  ],
  // watch: true,
    output: {
      path: path.resolve('./assets/webpack_bundles/'),
      filename: "[name]-[hash].js"
  },
    // mode: 'development',
    devtool: 'inline-source-map',
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        }
      ]
    },
    plugins: [
      new BundleTracker({filename: './webpack-stats.json'}),
      new CleanWebpackPlugin(),
   ],
    resolve: {
        //tells webpack where to look for modules
        modules: [path.join(__dirname, "assets"), "node_modules"],
        //extensions that should be used to resolve modules
        extensions: ['.js', '.jsx']
    }
}
