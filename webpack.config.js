var path = require('path');
var UglifyJsPlugin = require('uglifyjs-webpack-plugin');
var MiniCssExtractPlugin = require('mini-css-extract-plugin');
var autoprefixer = require('autoprefixer');
var devMode = process.env.NODE_ENV !== 'production';
var webpack = require('webpack');

var conf = {
    entry: {
        index: './static/js/index.js',
        post: './static/js/post.js',
        dev: './static/js/dev.js'
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'static/bundle/')
    },
    devServer:{
        overlay: true
    },
    optimization: {
        minimizer: [
            new UglifyJsPlugin()
        ],
        splitChunks: {
            cacheGroups: {
                styles: {
                    name: 'styles',
                    test: /\.css$/,
                    chunks: 'all',
                    enforce: true
                }
            }
        }
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: '/node_modules/'
            },
            {
                test: /\.(scss|css)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            minimize: {
                                safe: true
                            },
                            autoprefixer: true,
                            importLoaders: 1
                        }
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            ident: 'postcss',
                            plugins: (loader) => [
                                require('autoprefixer')({
                                    browsers:['>1%', 'last 4 version']
                                }),
                                require('cssnano')
                            ]
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {}
                    }
                ]
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'fonts/'
                    }
                }]
            },
            {
                test: /\.(png|jpg|gif)$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'images/'
                    }
                }]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css'
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery'
        }),
    ]
};

module.exports = (env, options)=>{
    var production = options.mode === 'production';
    conf.devtool = production ? false :'eval-sourcemap';
    // conf.devtool = production ? 'source-map' :'eval-sourcemap';
    return conf;
}