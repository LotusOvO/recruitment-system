<template>
  <div>
    <div class="accordion" id="accordionPanelsStayOpenExample">
      <div class="accordion-item">
        <h2 class="accordion-header" id="panelsStayOpen-headingOne">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                  data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="false"
                  aria-controls="panelsStayOpen-collapseOne">
            热门岗位统计
          </button>
        </h2>
        <div id="panelsStayOpen-collapseOne" class="accordion-collapse collapse"
             aria-labelledby="panelsStayOpen-headingOne">
          <div class="accordion-body">
            <button class="btn-primary btn" @click="drawPositionChart()">获取数据</button>
            <div class="chartOne" ref="chartOne" style="height:300px;width: auto;"></div>
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="panelsStayOpen-headingTwo">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                  data-bs-target="#panelsStayOpen-collapseTwo" aria-expanded="false"
                  aria-controls="panelsStayOpen-collapseTwo">
            应聘状态统计
          </button>
        </h2>
        <div id="panelsStayOpen-collapseTwo" class="accordion-collapse collapse"
             aria-labelledby="panelsStayOpen-headingTwo">
          <div class="accordion-body">
            <button class="btn-primary btn" @click="drawRecruitmentChart">获取数据</button>
            <div class="chartTwo" ref="chartTwo" style="height:300px;width: auto;"></div>
          </div>
        </div>
      </div>
<!--      <div class="accordion-item">-->
<!--        <h2 class="accordion-header" id="panelsStayOpen-headingThree">-->
<!--          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"-->
<!--                  data-bs-target="#panelsStayOpen-collapseThree" aria-expanded="false"-->
<!--                  aria-controls="panelsStayOpen-collapseThree">-->
<!--            统计-->
<!--          </button>-->
<!--        </h2>-->
<!--        <div id="panelsStayOpen-collapseThree" class="accordion-collapse collapse"-->
<!--             aria-labelledby="panelsStayOpen-headingThree">-->
<!--          <div class="accordion-body">-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: "DataPage",
  data() {
    return {
      positionData: {name: [], value: [], id: []},
      positionChart: null,
      recruitmentData: {status: [], value: []},
      recruitmentChart: null,
    }
  },
  methods: {
    drawPositionChart(num = 10) {
      const path = '/count/positions/' + num;
      this.$axios.get(path)
          .then((response) => {
            this.positionData = {name: [], value: [], id: []}
            for (let key in response.data) {
              this.positionData.name.push(response.data[key].name)
              this.positionData.value.push(response.data[key].number)
              this.positionData.id.push(response.data[key].id)
            }
            if (this.positionChart) {
              this.positionChart.dispose()
            }
            this.positionChart = echarts.init(this.$refs.chartOne);
            let option = {
              xAxis: {
                data: this.positionData.name
              },
              yAxis: {
                axisLabel: {
                  formatter: '{value}人'
                },
                minInterval: 1
              },
              tooltip: {
                trigger: 'item',
              },
              series: [{
                type: 'bar',
                data: this.positionData.value
              }]
            }
            this.positionChart.setOption(option)
            this.positionChart.on('click', (param) => {
              // console.log(param)
              this.$emit('searchName', param.name)
            })
          })
          .catch((error) => {
            console.log(error)
          })
    },
    drawRecruitmentChart() {
      const path = '/count/status';
      this.$axios.get(path)
          .then((response) => {
            this.recruitmentData = {status: [], value: []};
            if (this.recruitmentChart) {
              this.recruitmentChart.dispose();
            }
            const status = ['流程终止', '待审', '初审', '一面', '二面', '入职'];
            const num = [-1, 0, 1, 2, 3, 4];
            for (let i = 0; i < num.length; ++i) {
              this.recruitmentData.status.push(status[i]);
              this.recruitmentData.value.push(response.data[num[i]]);
            }
            this.recruitmentChart = echarts.init(this.$refs.chartTwo);
            let option = {
              xAxis: {
                data: this.recruitmentData.status
              },
              yAxis: {
                axisLabel: {
                  formatter: '{value}人'
                },
                minInterval: 1
              },
              tooltip: {
                trigger: 'item',
              },
              series: [{
                type: 'bar',
                data: this.recruitmentData.value
              }]
            }
            this.recruitmentChart.setOption(option)
          })
          .catch((error) => {
            console.log(error)
          })
    }
  }
}
</script>

<style scoped>

</style>