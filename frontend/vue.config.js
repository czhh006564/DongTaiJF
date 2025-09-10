const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // 开发服务器配置
  devServer: {
    port: 8082,
    host: 'localhost',
    open: true,
    // 代理API请求到后端
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true,
        secure: false,
        logLevel: 'debug'
      }
    }
  },
  
  // 生产环境配置
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  
  // CSS配置
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  },
  
  // 插件配置
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  }
})