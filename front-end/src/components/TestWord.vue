<template>
  <div>
    <h3 class="container">首页</h3>
    <p>{{ message }}</p>
    <button class="btn btn-warning" >send</button>
    <button class="btn btn-danger" >test button</button>
  </div>
</template>

<script>
import store from "@/store";
export default {
  name: "TestWord",
  data() {
    return {
      message:'123'
    }
  },
  methods:{
    getMessage(){
      const path = '/test1'
      this.$axios.get(path)
          .then((res)=>{
            this.message = res.data;
          })
          .catch((error)=>{
            console.error(error);
          })
    },
    testFunc(){
      const path ='/confirm/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb25maXJtIjo1LCJleHAiOjE2NjAxMDEzNzIsImlhdCI6MTY2MDA5OTU3Mn0.fRK-kMeL3tO6IubnznzZZoE0KQdNwhve7KhhkCsAi7A'
      this.$axios.get(path)
          .then((response) =>{
            console.log(response)
          })
          .catch((error) =>{
            console.log(error)
          })
    },
    send(){
      const path = '/confirm/' + store.state.user_id;
      this.$axios.post(path)
          .then((response) =>{
            console.log(response)
          })
          .catch((error) =>{
            console.log(error)
          })
    }
  },
  created() {
    this.getMessage()
  }
}
</script>

<style scoped>

</style>