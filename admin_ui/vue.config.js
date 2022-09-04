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
        },
        // This is required if running on Windows Subsystem for Linux (it
        // seems like GitHub Actions uses this.
        watchOptions: {
            aggregateTimeout: 300,
            poll: 1000
        },
    }
}
