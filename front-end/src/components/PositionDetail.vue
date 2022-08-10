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
        <button class="btn btn-primary" v-on:click="applyPosition(position.id)">应聘该岗位</button>
      </div>
    </div>
  </div>
</template>

<script>
import store from "@/store";
// import qs from 'qs'
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
    },
    applyPosition(position_id){
      const user_id = store.state.user_id;
      const path = '/recruit/' + user_id;
      this.$axios.post(path, {position_id: position_id})
          .then((response)=>{
            this.$toasted.success('应聘成功')
            console.log(response.data)
          })
          .catch((error) =>{
            this.$toasted.error(error.response.data.message)
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