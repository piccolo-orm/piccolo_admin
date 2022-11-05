module.exports = {
    lintOnSave: false,
    outputDir: '../piccolo_admin/dist',
    publicPath: './',

    devServer: {
        port: 3000,
        proxy: {
            '^/api': {
                target: 'http://127.0.0.1:8000'
            },
            '^/public': {
                target: 'http://127.0.0.1:8000'
            }
        },
    }
}
