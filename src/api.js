const express = require('express')
const child_process = require('child_process')
const fs = require('fs')
const remoteModules = require('../module')
const path = require('path')
const { json } = require('body-parser')

const router = express.Router()
const logFilePath = 'log.txt'

/**
 * 通用方法
 */
// 获取时间戳
const dateString = () => {
  const date = new Date()
  return `TIME: ${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
}
// 记录日志
async function writeLog(content) {
  fs.appendFileSync(logFilePath, `${dateString()} ${content}\n`)
}
// 远程模型代理
function proxyModulePath(modulePath, module, cb) {
  fs.exists(`${modulePath}`, exists => {
    if (!exists) {
      // 本地文件不存在时 检查远程链接是否可用
      if (remoteModules[module]) {
        modulePath = `${remoteModules[module]}`
      }
    }
    cb(modulePath)
  })
}

/**
 * 测试
 */
router.get('/test', (req, res) => {
  res.json({ msg: 'API works!' })
  writeLog("API TEST OK")
})

/**
 * 训练
 */
router.get('/train', async (req, res) => {
  const { module } = req.query
  if (!module) {
    res.json({ errmsg: '必填module参数' })
    writeLog("api/train 未填module参数")
    return
  }
  let modulePath = `modules/${module}`
  proxyModulePath(modulePath, module, doTraining)
  /**
   * 执行训练
   */
  function doTraining(modulePathAfterProxy) {
    fs.exists(`${modulePathAfterProxy}/train.py`, exists => {
      if (!exists) {
        writeLog(`api/train/${module} 找不到指定module`)
        res.json({ errmsg: 'module不存在' })
      } else {
        res.json({ msg: '正在训练，请使用/log接口查看训练结果' })
        const id = parseInt(Math.random() * 1e5)
        writeLog(`api/train/${module}/id:${id} 开始训练模型`)

        // 写入时间戳
        fs.writeFileSync(
          `${modulePathAfterProxy}/trainLog.txt`,
          `${dateString()} 正在训练中... \n`
        )
        try {
          child_process.exec(`d: && cd ${modulePathAfterProxy} && python3 train.py`, (err, stdout, stderr) => {
            if (err) {
              fs.appendFileSync(`${modulePathAfterProxy}/trainLog.txt`, `${dateString()} python执行阶段错误 \n ${String(err)}`)
              writeLog(`api/train/${module}/id:${id} 失败:python执行出现错误\n${err.toString()}`)
            }
            else
              fs.appendFileSync(`${modulePathAfterProxy}/trainLog.txt`, `${dateString()} 训练完成 \n ${stdout}`)
            writeLog(`api/train/${module}/id:${id} 训练完成`)

          })
        } catch (error) {
          fs.appendFileSync(`${modulePathAfterProxy}/trainLog.txt`, `${dateString()} python执行阶段错误 \n ${String(error)}`)
        }

      }
    })
  }

})
/**
 * 获取训练日志
 */
router.get('/log', (req, res) => {
  const { module } = req.query
  if (!module) {
    res.json({ errmsg: '必填module参数' })
    writeLog("api/log 未填module参数")
    return
  }
  let modulePath = `modules/${module}`

  proxyModulePath(modulePath, module, getLog)

  function getLog(modulePath) {
    fs.exists(`${modulePath}/trainLog.txt`, exists => {
      if (!exists) {
        res.json({ errmsg: 'module不存在或未进行训练' })
        writeLog(`api/log/${module} 找不到指定module或没有进行训练`)
      } else {
        // const data = fs.readFileSync(`${modulePath}/trainLog.txt`)
        writeLog(`api/log/${module} 发送日志成功`)
        res.writeHead(200, { 'Content-Type': 'text/html;charset=utf-8' })
        res.sendfile(`${modulePath}/trainLog.txt`)
      }
    })
  }

})

router.get('/logs', (req, res) => {
  const { type } = req
  if (type && type === 'clear') child_process.exec('rm log.txt & touch log.txt')
  //  writeLog('发送Log成功')
  res.sendfile('log.txt')
})

router.post('/predict', (req, res) => {
  const { data, module } = req.body
  if (!module) {
    res.json({ errmsg: '必填module' })
    writeLog("api/predict 未填module参数")
    return
  }
  let modulePath = `modules/${module}`

  proxyModulePath(modulePath, module, doingPredict)

  function doingPredict(modulePath) {
    fs.exists(`${modulePath}/model.py`, exists => {
      if (!exists) {
        res.json({ errmsg: 'module不存在' })
        writeLog(`api/predict/${module} 未找到指定module`)
      } else {
        if (data) fs.writeFileSync(`${modulePath}/predictData.txt`, data, { encoding: 'utf8' })
        try {
          child_process.exec(`d: && cd ${modulePath} && python3 model.py`, (err, stdout, stderr) => {
            if (err) {
              res.json({ errmsg: 'python执行阶段错误:' + String(err) })
              writeLog(`api/predict/${module} 失败:python执行出现错误\n${String(err)}`)
              return
            }
            const data = fs.readFileSync(`${modulePath}/result/predictResult.txt`, { encoding: 'utf-8' })
            res.json({ data: '预测成功，结果为:' + data.toString().trim() })
            console.log(String(data))
            writeLog(`api/predict/${module} 预测成功 结果${data.toString()}`)
          })
        } catch (error) {
          res.json({ errmsg: 'python执行阶段错误:' + String(error) })
        }
      }
    })
  }

})


router.post('/predictExt', (req, res) => {
  const { data, module } = req.body
  if (!module) {
    res.json({ errmsg: '必填module' })
    writeLog("api/predict 未填module参数")
    return
  }
  let modulePath = `modules/${module}`

  proxyModulePath(modulePath, module, doingPredict)

function doingPredict(modulePath) {
    fs.exists(`${modulePath}/model.py`, exists => {
      if (!exists) {
        res.json({ errmsg: 'module不存在' })
        writeLog(`api/predict/${module} 未找到指定module`)
      } else {
        if (data) fs.writeFileSync(`${modulePath}/predictData.txt`, data, { encoding: 'utf8' })
        // 创建唯一标识id
        const id = `${(new Date()).getTime()}`
        try {
          child_process.exec(`cd EXT_RESULTS && mkdir ${id}`)
          // child_process.exec(`d: && cd ${modulePath} && python3 model.py`, (err, stdout, stderr) => {
          child_process.exec(`cd ${modulePath} && python3 model.py --id '${id}'`, (err, stdout, stderr) => {})
        } catch (error) {
          res.json({ errmsg: 'python执行阶段错误:' + String(error) })
        }
        res.json({
          message: '结果请点击url查看',
          url: `http://117.73.9.94:8080/#/?module=${module}&id=${id}`
        })
      }
    })
  }
})

router.get('/fetchExtResults', (req,res) => {
  const { id } = req.query
  const rootPath = `./EXT_RESULTS/${id}`
  const dir =fs.readdirSync(rootPath)
  let resultPath = '', imgMap = {}
  // 文件处理 分为result.txt 和 图片类型
  dir.forEach(dirPath => {
    if(dirPath === 'result.txt') resultPath = `${rootPath}/result.txt`
    else if(dirPath.endsWith('.jpg') || dirPath.endsWith('.png')){
      imgMap[dirPath.split('.')[0]] = `http://117.73.9.94:7277/ext/${id}/${dirPath}`
    }
  })
  if(!resultPath) res.json({ type: 0, message: '未出现结果' })
  else {
    const result = {}
    const resultInline = fs.readFileSync(resultPath).toString().split('\n')
    resultInline.forEach(line => {
      const [code, res] = line.split(' ')
      if(!imgMap) return
      result[code] = {
        id: parseInt(code,10) + 1,
        result: res,
        img: imgMap[code]
      }
    })
    res.json({ type: 1, result })
  }
})
module.exports = router