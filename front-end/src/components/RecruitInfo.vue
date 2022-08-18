<template>
  <div>
    <div v-for="item in recruitments" :key="item.id" class="row tmp">
      <div class="card position_card container card1">
        <div class="card-body">
          <p class="card-text">岗位名称：{{ item.name }}</p>
          <p class="card-text">工作部门：{{ item.department }}</p>
          <p class="card-text">工作地点：{{ item.location }}</p>
          <p class="card-text">进度：{{ status[item.status] }}</p>
          <div class="progress col-12">
            <div class="progress-bar progress-bar-striped" role="progressbar" :class="statusClass[item.status]"></div>
          </div>
          <div class="col-12 row">
            <div class="col-sm-1"></div>
            <p class="col-sm-2">待审</p>
            <p class="col-sm-2">初审</p>
            <p class="col-sm-2">一面</p>
            <p class="col-sm-2">二面</p>
            <div class="col-sm-1"></div>
            <p class="col-sm-2" v-show="item.status !== 4">流程终止</p>
            <p class="col-sm-2" v-show="item.status === 4">入职</p>
          </div>
          <button class="btn btn-primary" v-on:click="deleteRecruitment(item.id)">取消应聘</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RecruitInfo",
  data() {
    return {
      recruitments: [],
      status: {
        0: '待审',
        1: '初审',
        2: '一面',
        3: '二面',
        4: '入职',
        '-1': '流程终止'
      },
      statusClass: {
        0: 'statusZero',
        1: 'statusOne',
        2: 'statusTwo',
        3: 'statusThree',
        4: 'statusFour',
        '-1': 'refuse'
      },
    }
  },
  methods: {
    getRecruitment(user_id) {
      const path = '/recruit/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.recruitments = response.data;
          })
          .catch((error) => {
            console.log(error)
          })
    },
    deleteRecruitment(position_id) {
      const path = '/recruit/' + this.$route.params.user_id;
      this.$axios.delete(path, {data: {position_id: position_id}})
          .then((response) => {
            this.$toasted.success('已取消应聘该岗位')
            this.recruitments = response.data;
          })
          .catch((error) => {
            this.$toasted.error('操作失败')
            console.log(error)
          })
    },
    addRecruitment(position_id) {
      const path = '/recruit/' + this.$route.params.user_id;
      this.$axios.post(path, {position_id: position_id})
          .then((response) => {
            this.recruitments = response.data;
          })
          .catch((error) => {
            console.log(error)
          })
    }
  },
  created() {
    const user_id = this.$route.params.user_id;
    this.getRecruitment(user_id);
  }
}
</script>

<style scoped>
.card1 {
  width: 70%;
}

.tmp {
  margin-top: 15px;
}

.refuse {
  width: 100%;
  --bs-bg-opacity: 1;
  background-color: rgba(var(--bs-danger-rgb),var(--bs-bg-opacity))!important;
}

.statusZero{
  width: 20%;
}
.statusOne{
  width: 40%;
}
.statusTwo{
  width: 60%;
}
.statusThree{
  width: 80%;
}
.statusFour{
  width: 100%;
  --bs-bg-opacity: 1;
  background-color: rgba(var(--bs-success-rgb),var(--bs-bg-opacity))!important;
}
</style>