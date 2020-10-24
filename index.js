const express = require('express')
const path = require('path')
const api = require('./src/api')
const app = express()
const extApp = express()

// 解析post请求中的body
const bodyParser = require('body-parser')

// 解析urlencoded和raw/json
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

// 路由接口文件：端口之上使用routes 当访问users/*** 就能找到该路由文件
app.all('*', function (req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type, Authorization');
  res.setHeader("Content-Type", "application/json;charset=utf-8");
  next();
});
/**
 * 接口：
 */
app.use('/api', api)
extApp.use('/ext', express.static(path.join(__dirname, 'EXT_RESULTS')));
extApp.use('/ext_page', express.static(path.join(__dirname, 'dist')));
extApp.use('/api', api)


const port = '6666'
const extPort = '7277'

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
})
extApp.listen(extPort, () => {
  console.log(`EXT Server running on port ${extPort}`)
})