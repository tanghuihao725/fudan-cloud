pm2 stop fudan-cloud

echo '从git上拉取最新代码'
git pull
echo '拉取代码完成'
echo '开始构建'
npm install
echo '构建完成'
echo '初始化module.js'
if [ -f 'module.js' ]; then
  echo 'module.js exist'
else
  cp modules/module-init.js module.js
fi
echo 'module.js 初始化完成'
echo '执行后台'
pm2 start index.js --name fudan-cloud