<template>
  <div>
    <form class="row" @submit.prevent="search(searchForm.user_name,searchForm.position_name)">
      <div class="col-md-1"></div>
      <input v-model="searchForm.user_name" class="col-md-3 col-form-control" id="user_name" type="text"
             placeholder="人员姓名">
      <div class="col-md-1"></div>
      <input v-model="searchForm.position_name" class="col-md-3 col-form-control" id="position_name" type="text"
             placeholder="岗位名称">
      <div class="col-md-1"></div>
      <button class="btn col-md-2 btn-outline-primary" type="submit">搜索</button>
    </form>
    <div v-for="(item,index) in relations" v-bind:key="index">
      <div class="card container card2">
        <div class="card-body">
          <p class="card-text">应聘人:{{ item.user.name }}</p>
          <p class="card-text">职位:{{ item.position.name }}</p>
          <p class="card-text">部门:{{ item.position.department }}</p>
          <p class="card-text">地点:{{ item.position.location }}</p>
          <p class="card-text">进度:{{ status[item.position.status] }}</p>
        </div>
        <div class="card-footer row">
          <button class="btn btn-primary col-md-4" data-bs-toggle="modal" data-bs-target="#staticBackdrop3"
                  v-on:click="getInformation(item.user.id)">查看应聘人资料
          </button>
          <div class="col-md-1"></div>
          <button class="btn btn-danger col-md-3" v-on:click="refuse(item.user.id,item.position.id)">流程终止</button>
          <div class="col-md-1"></div>
          <button class="btn btn-warning col-md-3" v-on:click="advance(item.user.id,item.position.id)">下一流程</button>
        </div>
      </div>
    </div>

    <div class="modal fade" id="staticBackdrop3" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">个人资料</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <h4>基本资料</h4>
            <div class="row block">
              <p class="col-md-6">姓名:{{ information.base_info.name }}</p>
              <p class="col-md-6">性别:{{ information.base_info.sex }}</p>
              <p class="col-md-6">民族:{{ information.base_info.race }}</p>
              <p class="col-md-6">电话号码:{{ information.base_info.phone_number }}</p>
              <p class="col-md-12">身份证:{{ information.base_info.id_number }}</p>
              <p class="col-md-12">地址:{{ information.base_info.address }}</p>
            </div>
            <hr>
            <h4>教育经历</h4>
            <div v-for="(item,index) in information.edu_info" :key="index + 'edu'" class="row block">
              <p class="col-md-12">学位:{{ item.degree }}</p>
              <p class="col-md-6">学校:{{ item.school }}</p>
              <p class="col-md-6">专业:{{ item.major }}</p>
              <p class="col-md-6">入学时间:{{ item.begin_date }}</p>
              <p class="col-md-6">入学时间:{{ item.end_date }}</p>
            </div>
            <hr>
            <h4>工作经历</h4>
            <div v-for="(item,index) in information.work_info" :key="index + 'work'" class="row block">
              <p class="col-md-6">工作单位:{{ item.company }}</p>
              <p class="col-md-6">工作职位:{{ item.position }}</p>
              <p class="col-md-6">入职时间:{{ item.begin_date }}</p>
              <p class="col-md-6">离职时间:{{ item.end_date }}</p>
              <p class="col-md-12">详细描述:{{ item.describe }}</p>
            </div>
            <hr>
            <h4>家庭关系</h4>
            <div v-for="(item,index) in information.fam_info" :key="index + 'fam'" class="row block">
              <p class="col-md-6">姓名:{{ item.name }}</p>
              <p class="col-md-6">工作:{{ item.work }}</p>
              <p class="col-md-6">与本人关系:{{ item.relation }}</p>
              <p class="col-md-6">联系电话:{{ item.phone_number }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "RecruitManage",
  data() {
    return {
      timer: null,
      searchForm: {
        user_name: '',
        position_name: ''
      },
      relations: [],
      status: {
        0: '待审',
        1: '初审',
        2: '一面',
        3: '二面',
        4: '入职',
        '-1': '流程终止'
      },
      information: {
        base_info: {},
        work_info: [],
        fam_info: [],
        edu_info: []
      }
    }
  },
  methods: {
    search(user_name = '', position_name = '') {
      let path = '/recruit/search';
      if (user_name !== '' && position_name !== '') {
        path += '?user_name=' + user_name + '&position_name=' + position_name;
      } else {
        if (user_name !== '') {
          path += '?user_name=' + user_name;
        }
        if (position_name !== '') {
          path += '?position_name=' + position_name;
        }
      }

      this.$axios.get(path)
          .then((response) => {
            this.relations = response.data;
          })
          .catch((error) => {
            console.log(error)
          })
    },
    getInformation(user_id) {
      let path = '/base_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.information.base_info = response.data;
          })

      path = '/edu_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.information.edu_info = response.data;
          })

      path = '/work_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.information.work_info = response.data;
          })

      path = '/fam_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.information.fam_info = response.data;
          })

    },
    advance(user_id, position_id) {
      const path = '/recruit/advance';
      this.$axios.put(path, {user_id: user_id, position_id: position_id});
      clearTimeout(this.timer);
      this.timer = setTimeout(()=>{this.search(this.searchForm.user_name, this.searchForm.position_name)},1000)
      this.$toasted.success('进入下一流程')

    },
    refuse(user_id, position_id) {
      const path = '/recruit/refuse';
      this.$axios.put(path, {user_id: user_id, position_id: position_id});
      clearTimeout(this.timer);
      this.timer = setTimeout(()=>{this.search(this.searchForm.user_name, this.searchForm.position_name)},1000)
      this.$toasted.success('已终止该流程')
    }
  },
  created() {
    this.search();
  }
}
</script>

<style scoped>
.card2 {
  margin-top: 15px;
}

.block {
  margin-top: 15px;
}
</style>