# fudan-cloud 测试平台后台使用说明 

** 基于node开发，所以需要安装node环境，可在node官网下载 **

# 运行准备

1. `git clone` ... 从仓库获取代码
2. `npm install` 安装依赖
3. `node index.js` 执行后台入口文件

# 接口文档

1. 训练 
GET 接口 `/api/train`
@query: module 必传 模型名
请求示例： http://localhost:6666/api/train?module=test

2. 预测
POST 接口 `/api/predict`
@query: 无
@body:
    module 必传 模型名
    data 模型输入数据
请求示例： http://localhost:6666/api/predict
body: module=test  data= 0 1 2 3 4 5
