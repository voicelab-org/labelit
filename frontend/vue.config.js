module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:8000/',
        //target: 'https://labelit.staging.hosting.call.watch/',
        //changeOrigin: true,
        secure: false,
        logLevel: "debug"
      },
    }
  },

  transpileDependencies: [
    'vuetify'
  ]
}
