<template>
  <div>
    <br>
    <h3 class="container">首页</h3>
    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel" style="width: 70%;margin:auto;">
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="10000">
          <img src="../assets/1.jpeg" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item" data-bs-interval="2000">
          <img src="../assets/2.jpg" class="d-block w-100" alt="...">
        </div>
        <div class="carousel-item">
          <img src="../assets/3.png" class="d-block w-100" alt="...">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls"
              data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls"
              data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
    <br>
    <h2>欢迎加入中国电信中山分公司</h2>
<!--    <button class="btn btn-warning">send</button>-->
<!--    <button class="btn btn-danger" @click="testFunc">test button</button>-->
  </div>
</template>

<script>
import store from "@/store";

export default {
  name: "TestWord",
  data() {
    return {
      message: '123'
    }
  },
  methods: {
    getMessage() {
      const path = '/test1'
      this.$axios.get(path)
          .then((res) => {
            this.message = res.data;
          })
          .catch((error) => {
            console.error(error);
          })
    },
    testFunc() {
      const path = '/count/department/10'
      this.$axios.get(path)
          .then((response) => {
            console.log(response)
          })
          .catch((error) => {
            console.log(error)
          })
    },
    send() {
      const path = '/confirm/' + store.state.user_id;
      this.$axios.post(path)
          .then((response) => {
            console.log(response)
          })
          .catch((error) => {
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