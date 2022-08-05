<template>
  <div>
    <form class="row g-3" @submit.prevent="setBaseInfo">
      <div class="col-md-6">
        <label for="name" class="form-label">姓名</label>
        <input v-model="base_info.name" type="text" class="form-control" id="name">
      </div>
      <div class="col-md-6">
        <label for="sex" class="form-label">性别</label>
        <input v-model="base_info.sex" type="text" class="form-control" id="sex">
      </div>
      <div class="col-md-6">
        <label for="race" class="form-label">民族</label>
        <input v-model="base_info.race" type="text" class="form-control" id="race">
      </div>
      <div class="col-md-6">
        <label for="id_number" class="form-label">身份证号</label>
        <input v-model="base_info.id_number" type="text" class="form-control" id="id_number">
      </div>
      <div class="col-md-6">
        <label for="phone_number" class="form-label">电话号码</label>
        <input v-model="base_info.phone_number" type="text" class="form-control" id="phone_number">
      </div>
      <div class="col-md-6">
        <label for="address" class="form-label">地址</label>
        <input v-model="base_info.address" type="text" class="form-control" id="address">
      </div>
      <button type="submit" class="btn btn-warning col-md-2 container">保存</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "BaseInfo",
  data() {
    return {
      base_info: {
        name: '',
        sex: '',
        race: '',
        id_number: '',
        phone_number: '',
        address: ''
      }
    }
  },
  methods: {
    getBaseInfo(user_id) {
      const path = '/base_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.base_info = response.data;
          })
          .catch((error) => {
            console.log(error)
          })
    },
    setBaseInfo() {
      const path = '/base_info/' + this.$route.params.user_id;
      this.$axios.put(path, this.base_info)
          .then((response) => {
            this.base_info = response.data;
          })
          .catch((error) => {
            console.log(error)
          })
    }
  },
  created() {
    const id = this.$route.params.user_id;
    this.getBaseInfo(id);
  }
}
</script>

<style scoped>
.btn{
  margin-top: 20px;
}
</style>