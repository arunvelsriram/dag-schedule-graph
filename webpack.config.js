const path = require('path');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');

const STATIC_DIR = path.resolve(__dirname, './dag_schedule_graph/static');
const BUILD_DIR = path.resolve(__dirname, './dag_schedule_graph/static/dist');

function isDevelopment(mode) {
    return mode === 'development';
}

module.exports = (env, options) => {
    const {mode} = options;
    return {
        devtool: isDevelopment(mode) ? 'source-map' : false,
        entry: {
            main: `${STATIC_DIR}/js/index.js`
        },
        output: {
            path: BUILD_DIR,
            filename: '[name].js'
        },
        externals: {
            moment: 'moment'
        },
        plugins: [
            new CleanWebpackPlugin()
        ]
    }
};
