module.exports = {
    lintOnSave: false,
    outputDir: '../piccolo_admin/dist',
    publicPath: './',

    devServer: {
        port: 3000,
        proxy: {
            '^/api': {
                target: 'http://localhost:8000'
            },
            '^/public': {
                target: 'http://localhost:8000'
            }
        }
    }
}
