const express = require('express')
const child_process = require('child_process')
const fs = require('fs')

const router = express.Router()

// 获取时间戳
const dateString = () => {
    const date = new Date()
    return `TIME: ${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
}


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
            // 写入时间戳
            fs.writeFileSync(
                `${modulePath}/trainLog.txt`,
                `${dateString()} 正在训练中... \n`
                )
            try {
                child_process.exec(`cd ${modulePath} && python3 train.py`, (err, stdout, stderr) => {
                    if(err){
                        fs.appendFileSync(`${modulePath}/trainLog.txt`, `${dateString()} python执行阶段错误 \n ${String(err)}`)
                    }
                    else 
                        fs.appendFileSync(`${modulePath}/trainLog.txt`, `${dateString()} 训练完成 \n ${stdout}`)
                })  
            } catch (error) {
                fs.appendFileSync(`${modulePath}/trainLog.txt`, `${dateString()} python执行阶段错误 \n ${String(error)}`)
            }
             
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
             try {
                child_process.exec(`cd ${modulePath} && python3 model.py`, (err, stdout, stderr) => {
                    if(err){
                        res.json({errmsg: 'python执行阶段错误:' + String(err)})
                        return
                    }
                    const data = fs.readFileSync(`${modulePath}/result/predictResult.txt`)
                    res.json({stdout, stderr, data: data.toString()})
                 })   
             } catch (error) {
                 res.json({errmsg: 'python执行阶段错误:' + String(error)})
             }
         }
     })
 })
 
 module.exports = router