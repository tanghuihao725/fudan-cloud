<template>
    <div class="result-item">
        <div class="id">
            图片编号：{{id}}
        </div>
        <div class="img-wrapper">
            原图
            <a :href="img" target="_blank">
                <img :src="img" class="img">
            </a>
            模型输出
        </div>
        <div class="result-wrapper" :style="{color: result==='有质量问题'?'red':'black'}">
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
    margin: 30px 0;
    display: flex;
    padding: 0 20%;
    align-items: center;
    justify-content: space-around;
    // border: 1px solid red;

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


}
</style>