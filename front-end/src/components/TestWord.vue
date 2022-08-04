<template>
  <div>
    <p>{{ message }}</p>
    <button type="button" class="btn btn-primary">abc</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "TestWord",
  data() {
    return {
      message:'123'
    }
  },
  methods:{
    getMessage(){
      const path = 'http://127.0.0.1:5000/api/test1'
      axios.get(path)
          .then((res)=>{
            this.message = res.data;
          })
          .catch((error)=>{
            console.error(error);
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