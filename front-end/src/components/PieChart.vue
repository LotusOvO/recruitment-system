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
  // computed:{
  //   sum : ()=>{
  //
  //     console.log(this.datas)
  //     return 0;
  //   }
  // },
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
      let sum = 0;
      for(let item in this.datas){
        sum += this.datas[item].value;
      }
      let option = {
        title: {
          zlevel: 0,
          x: 'center',
          y: 'center',
          text : "总" + sum + "人"
        },
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