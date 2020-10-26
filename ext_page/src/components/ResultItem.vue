<template>
    <div class="result-item">
       
        <div class="img-wrapper row">
            原图
            <a :href="img" target="_blank">
                <img :src="img" class="img">
            </a>
            模型输出
        </div>
        <div class="id row">
            图片编号：{{id}}
        </div>
        <div class="result-wrapper row" :style="{color: result.indexOf('无')== -1?'#f40':'teal'}">
            {{result}}
        </div>
         
        

    </div>
</template>

<script>
import QRCode from 'qrcodejs2'

export default {
    props: ['id', 'result', 'img'],
    methods:{
        qrcode(){
            let that = this
            let qrcode = new QRCode('qrcode',{
                width: 124,
                height: 124,
                text: this.img,
            })
        }
    },
    mounted(){
        // this.qrcode()
    },
    components:{
        QRCode
    }
}
</script>

<style lang="less" scoped>
.result-item{
    display: flex;
    flex-direction: column;
    width: 19%;
    padding: 0 3%;
    margin-top: 30px;

    .img-wrapper{
        display: flex;
        align-items: center;
        font-size: 8px;
        color: #666;
    }
    .img{
        height: 200px;
        margin: 0 5px;
    }
    .row{
        margin-bottom: 10px;
        text-align: center;
    }
}
</style>