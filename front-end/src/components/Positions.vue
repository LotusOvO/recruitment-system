<template>
  <div class="row" style="width: 70%;margin: auto">
    <div v-for="item in positions" :key="item.id" class="col-lg-6">
      <br>
      <div class="card position_card container">
        <div class="card-body">
          <p class="card-text">岗位名称：{{ item.name }}</p>
          <p class="card-text">工作部门：{{ item.department }}</p>
          <p class="card-text">工作地点：{{ item.location }}</p>
          <router-link :to="{ name: 'positionDetail', params:{position_id : item.id} } " class="btn btn-primary">查看详情
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "PositionPage",
  data() {
    return {
      positions: []
    }
  },
  watch:{
    '$route':{
      handler(newVal){
          this.searchPosition(newVal.query.name)
      }
    }
  },
  methods: {
    getPositions() {
      const path = '/recruitment'
      this.$axios.get(path)
          .then((response) => {
            this.positions = response.data
          })
          .catch((error) => {
            console.log(error.response)
          })
    },
    searchPosition(name = '') {
      let path = '/recruitment/search';
      if (name !== '') {
        path += '?name=' + name;
      }
      this.$axios.get(path)
          .then((response) => {
            this.positions = response.data
          })
          .catch((error) => {
            console.log(error.response)
          })
    }
  },
  created() {
    if (this.$route.query.name) {
      this.searchPosition(this.$route.query.name)
    } else {
      this.getPositions();
    }
  }
}
</script>

<style scoped>
.position_card {
  /*width: 50%;*/
  border-radius: 10px;
}
</style>