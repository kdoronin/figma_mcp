const path = require('path');

module.exports = {
  entry: {
    code: './src/main.ts', // Main plugin code
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
  },
  // This is necessary because Figma's 'eval' works differently than normal eval
  devtool: false,
};