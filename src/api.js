const express = require('express')
const child_process = require('child_process')
const fs = require('fs')

const router = express.Router()


/**
 * 测试
 */
 router.get('/test', (req, res) => {
     res.json({ msg: 'API works!'})
 })

 router.get('/train', (req, res) => {
    const { module } = req.query
    if(!module){
          res.json({errmsg: '必填module参数'})
          return 
        } 
    const path = `modules/${module}/train.py`
    fs.exists(path, exists => {
        if(!exists){
            res.json({errmsg: 'module不存在'})
        }else{
            child_process.exec(`python3 ${path}`, (err, stdout, stderr) => {
                if(err) res.json({ errmsg: 'ERROR' })
                res.json({stdout, stderr})
            })   
        }
    })
 })

 router.post('/predict', (req, res) => {
     const { data="NO DATA", module } = req.body
     if(!module){
          res.json({errmsg: '必填module参数'})
          return 
        } 
     const modulePath = `modules/${module}`
     fs.exists(`${modulePath}/test.py`, exists => {
         if(!exists){
            res.json({errmsg: 'module不存在'})
         }else{
             fs.writeFileSync(`${modulePath}/prediction.txt`, data)
             child_process.exec(`python3 ${modulePath}/test.py`, (err, stdout, stderr) => {
                if(err) res.json({ errmsg: 'ERROR' })
                const data = fs.readFileSync(`${modulePath}/result.txt`)
                res.json({stdout, stderr, data: data.toString()})
             })
         }
     })
 })
 
 module.exports = router