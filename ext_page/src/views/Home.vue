<template>
  <div class="home">
    <p class="code">{{ module }}/{{ id }}</p>
    <div class="info">模型名称: {{ module }}</div>

    <div class="empty-type" v-if="!resultsContent && statu === 0">
      <img src="../assets/loading.gif" class="loading" />
      <p class="tip">正在运行中,请稍后 {{ showTimePass }}s</p>
    </div>

    <div v-else>
      <div class="waiting-tip" >
        <img v-show="statu === 1" src="../assets/loading.gif" class="mini-loading" />
        <p :style="{color: statu === 1 ? 'tomato' : 'teal'}">
        {{ statu === 1 ? `程序运行中，等待结果` : '已完成'}}
        {{showTimePass}}
        s
        </p>
      </div>
      <div class="result-content">
        <ResultItem
          v-for="item in resultData"
          :key="item.id"
          :id="item.id"
          :result="item.result"
          :img="item.img"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ResultItem from "@/components/ResultItem.vue";
const baseUrl =
  process.env.NODE_ENV === "development" ? "api/" : "http://117.73.9.94:7277";

export default {
  data() {
    return {
      module: this.$route.query.module || "ERROR_MODULE_NAME",
      id: this.$route.query.id || "ERROR_MODULE_ID",
      statu: 0, // 0未出结果 1等待中 2全部成功
      showTimePass: 0,
      resultsContent: null,
    };
  },
  computed: {
    timePassed() {
      const timeSec = (new Date().getTime() - parseInt(this.id)) / 1000;
      return Math.floor(timeSec);
    },
    resultData() {
      if (!this.resultsContent) return [];
      return Object.keys(this.resultsContent).map((id) => ({
        ...this.resultsContent[id],
      }));
    },
  },
  mounted() {
    console.log(process.env.NODE_ENV);
    const clock = setInterval(() => {
      this.showTimePass = this.computeTimePass();
      this.getExt().then((data) => {
        const { type, result, end } = data?.data;
        if (type === 1) {
          this.resultsContent = result;
          this.statu = end ? 2 : 1;
          if (end) clearInterval(clock);
        }
      });
    }, 1000);
  },
  methods: {
    computeTimePass() {
      const timeSec = (new Date().getTime() - parseInt(this.id)) / 1000;
      return Math.floor(timeSec);
    },
    getExt() {
      return axios.get(`${baseUrl}/api/fetchExtResults?id=${this.id}`)
      return new Promise((resolve, reject) => {
        // resolve({data: {type: 0}})
        resolve({
          data: {
            type: 1,
            end: true,
            result: {
              0: {
                result: "无质量问题",
                img: "http://localhost:7277/ext/1603504680243/0.jpg",
              },
              1: {
                result: "有质量问题",
                img: "http://localhost:7277/ext/1603504680243/1.jpg",
              },
            },
          },
        });
      });
    },
  },
  components: {
    ResultItem,
  },
};
</script>

<style lang="less" scoped>
.home {
  width: 100%;
  height: 98vh;

  max-width: 1200px;
  margin: 0 auto;
  .code {
    text-align: left;
    font-size: 8px;
    color: #666;
  }
  .info {
    margin: 60px 0;
    font-size: 30px;
  }

  .empty-type {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .loading {
      width: 50%;
      max-width: 400px;
    }
  }

  .waiting-tip {
    .mini-loading {
      width: 4em;
    }
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .result-content {
    width: 100%;
    border: 3px solid black;
    min-height: 400px;
    border-radius: 10px;
    display: flex;
    flex-wrap: wrap;
  }
}
</style>