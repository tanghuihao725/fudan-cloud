const express = require('express')
const path = require('path')
const api = require('./src/api')
const app = express()

// 解析post请求中的body
const bodyParser = require('body-parser')

// 解析urlencoded和raw/json
app.use(bodyParser.urlencoded({extended:false}))
app.use(bodyParser.json())

// 路由接口文件：端口之上使用routes 当访问users/*** 就能找到该路由文件

/**
 * 接口：
 */
app.use('/api', api)

const port = '6666'

app.listen(port, ()=>{
    console.log(`Server running on port ${port}`)
})