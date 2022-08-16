<template>
  <div id="myChart" style="width: 400px;height: 400px;margin: auto;">

  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: "PieChart",
  props: ['datas'],
  data() {
    return {
      myChart:null,
    }
  },
  // mounted() {
  //   this.$nextTick(()=>{
  //     this.getPie();
  //   })
  // },
  watch:{
    datas:function(){
      this.getPie();
    }
  },
  methods: {
    getPie() {
      // console.log(this.datas)
      if(this.myChart){
        this.myChart.dispose();
      }
      this.myChart = echarts.init(document.getElementById('myChart'))
      let option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}:{c} ({d}%)'
        },
        series: {
          name: '各流程人数',
          type: 'pie',
          radius: ['25%', '50%'],
          center: ['50%', '50%'],
          data: this.datas,
          itemStyle: {
              labelLine: {
                show: true,
              }
          }
        }
      }
      this.myChart.setOption(option)
    }
  }
}
</script>

<style scoped>

</style>