<template>
  <div>
    <br>
    <div class="card position_card container">
      <div class="card-body">
        <p class="card-text">岗位名称：{{ position.name }}</p>
        <p class="card-text">工作部门：{{ position.department }}</p>
        <p class="card-text">工作地点：{{ position.location }}</p>
        <p class="card-text">工作要求：{{ position.requirement }}</p>
        <p class="card-text">工作描述：{{ position.describe }}</p>
        <router-link to="" class="btn btn-primary">应聘该岗位</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PositionDetail",
  data() {
    return {
      position: {
        name: '',
        id: '',
        department: '',
        location: '',
        describe: '',
        requirement: ''
      }
    }
  },
  methods: {
    getPositionDetail(id) {
      const path = '/recruitment/' + id;
      this.$axios.get(path)
          .then((response) => {
            this.position = response.data
          })
          .catch((error) => {
            console.log(error)
          })
    }
  },
  created() {
    const position_id = this.$route.params.position_id;
    this.getPositionDetail(position_id);
  }
}
</script>

<style scoped>
.position_card{
  width: 70%;
  border-radius: 10px;
}
</style>