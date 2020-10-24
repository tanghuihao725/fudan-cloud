module.exports = {
    devServer:{
        proxy:{
            '/api': {
                target: 'http://localhost:7277',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
}