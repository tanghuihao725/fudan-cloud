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

 /**
  * 训练
  */
 router.get('/train', (req, res) => {
    const { module } = req.query
    if(!module){
          res.json({errmsg: '必填module参数'})
          return 
        } 
    const modulePath = `modules/${module}`

    fs.exists(`${modulePath}/train.py`, exists => {
        if(!exists){
            res.json({errmsg: 'module不存在'})
        }else{
            res.json({msg: '正在训练，请使用/log接口查看训练结果'})
            const date = new Date()
            // 写入时间戳
            fs.writeFileSync(
                `${modulePath}/trainLog.txt`,
                `TIME: ${date.toLocaleDateString()} ${date.toLocaleTimeString()}\n`
                )
            child_process.exec(`cd ${modulePath} && python3 train.py`, (err, stdout, stderr) => {
                if(err) res.json({ errmsg: err })
                // res.json({stdout, stderr})
                fs.appendFileSync(`${modulePath}/trainLog.txt`, stdout)
            })   
        }
    })
 })
 /**
  * 获取训练日志
  */
 router.get('/log', (req, res) => {
    const { module } = req.query
    if(!module){
        res.json({errmsg: '必填module和data参数'})
        return
    } 
    const modulePath = `modules/${module}`
    fs.exists(`${modulePath}/trainLog.txt`, exists => {
        if(!exists){
            res.json({errmsg: 'module不存在或未进行训练'})
        }else{
            // const data = fs.readFileSync(`${modulePath}/trainLog.txt`)
            res.sendfile(`${modulePath}/trainLog.txt`)
        }
    })
 })

 router.post('/predict', (req, res) => {
     const { data, module } = req.body
     if(!module || !data){
          res.json({errmsg: '必填module和data参数'})
          return 
        } 
     const modulePath = `modules/${module}`
     fs.exists(`${modulePath}/model.py`, exists => {
         if(!exists){
            res.json({errmsg: 'module不存在'})
         }else{
             fs.writeFileSync(`${modulePath}/predictData.txt`, data)
             child_process.exec(`cd ${modulePath} && python3 model.py`, (err, stdout, stderr) => {
                if(err) res.json({ errmsg: err })
                const data = fs.readFileSync(`${modulePath}/result/predictResult.txt`)
                res.json({stdout, stderr, data: data.toString()})
             })
         }
     })
 })
 
 module.exports = router