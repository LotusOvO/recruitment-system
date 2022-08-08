<template>
  <div>
    <div class="work-card" v-for="work in works" :key="work.id">
      <form class="row g-3" @reset="setWorkInfo(work.id)" @submit.prevent="deleteWorkInfo(work.id)">
        <div class="col-md-6">
          <label for="company" class="form-label">工作单位</label>
          <input v-model="work.company" type="text" class="form-control" id="company">
        </div>
        <div class="col-md-6">
          <label for="position" class="form-label">工作职位</label>
          <input v-model="work.position" type="text" class="form-control" id="position">
        </div>
        <div class="col-md-6">
          <label for="begin_date" class="form-label">入职时间</label>
          <input v-model="work.begin_date" type="text" class="form-control" id="begin_date">
        </div>
        <div class="col-md-6">
          <label for="end_date" class="form-label">离职时间</label>
          <input v-model="work.end_date" type="text" class="form-control" id="end_date">
        </div>
        <div class="col-md-12">
          <label for="describe" class="form-label">具体描述</label>
          <textarea v-model="work.describe" type="text" class="form-control" id="describe"></textarea>
        </div>
        <button type="reset" class="btn btn-warning col-md-2 container save-btn">保存修改</button>
        <button type="submit" class="btn btn-danger col-md-2 container save-btn">删除</button>
      </form>
    </div>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary add-btn" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
      新增工作经历
    </button>
    <!-- Modal -->
    <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">新增工作经历</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="row g-3">
              <div v-if="workForm.error > 0" class="col-md-12">
                <p>{{ workForm.errorInfo }}</p>
              </div>
              <div class="col-md-6">
                <label for="company" class="form-label">工作单位</label>
                <input v-model="workForm.company" type="text" class="form-control" id="company">
              </div>
              <div class="col-md-6">
                <label for="position" class="form-label">工作职位</label>
                <input v-model="workForm.position" type="text" class="form-control" id="position">
              </div>
              <div class="col-md-6">
                <label for="begin_date" class="form-label">入职时间</label>
                <input v-model="workForm.begin_date" type="text" class="form-control" id="begin_date">
              </div>
              <div class="col-md-6">
                <label for="end_date" class="form-label">离职时间</label>
                <input v-model="workForm.end_date" type="text" class="form-control" id="end_date">
              </div>
              <div class="col-md-12">
                <label for="describe" class="form-label">具体描述</label>
                <textarea v-model="workForm.describe" type="text" class="form-control" id="describe"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" v-on:click="addWorkInfo">添加</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WorkInfo",
  data() {
    return {
      works: [],
      workForm: {
        company: '',
        position: '',
        begin_date: '',
        end_date: '',
        describe: '',
        errors: 0,
        errorInfo: []
      }
    }
  },
  methods: {
    getWorkInfo(user_id) {
      const path = '/work_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.works = response.data;
          })
          .catch((error) => {
            console.log(error);
          })
    },
    setWorkInfo(work_id) {
      const path = '/work_info/' + this.$route.params.user_id;
      for (let i = 0; i < this.works.length; i++) {
        if (this.works[i].id === work_id) {
          this.$axios.put(path, this.works[i])
              .then((response) => {
                this.works = response.data;
              })
              .catch((error) => {
                console.log(error)
              })
          break;
        }
      }
    },
    deleteWorkInfo(work_id) {
      const path = '/work_info/' + this.$route.params.user_id;
      this.$axios.delete(path, {data: {id: work_id}})
          .then((response) => {
            this.works = response.data;
          })
          .catch((error) => {
            console.log(error);
          })
    },
    addWorkInfo() {
      const path = '/work_info/' + this.$route.params.user_id;
      if (this.workForm.company === '') {
        this.workForm.errors++;
        this.workForm.errorInfo += "请填写工作单位"
      }
      if (this.workForm.position === '') {
        this.workForm.errors++;
        this.workForm.errorInfo += "请填写工作职位"
      }
      if (this.workForm.begin_date === '') {
        this.workForm.errors++;
        this.workForm.errorInfo += "请填写入职时间"
      }
      if (this.workForm.end_date === '') {
        this.workForm.errors++;
        this.workForm.errorInfo += "请填写离职时间"
      }
      console.log(this.workForm.errors)
      if (this.workForm.errors === 0) {
        console.log("46546546554")
        this.$axios.post(path, {
          company: this.workForm.company,
          position: this.workForm.position,
          begin_date: this.workForm.begin_date,
          end_date: this.workForm.end_date,
          describe: this.workForm.describe
        })
            .then((response) => {
              this.works = response.data;
            })
            .catch((error) => {
              console.log(error)
            })
      }
    }
  },
  created() {
    const user_id = this.$route.params.user_id;
    this.getWorkInfo(user_id);
  }
}
</script>

<style scoped>
.save-btn {
  margin-top: 15px;
}

.add-btn {
  margin-top: 15px;
}

.work-card {
  margin-bottom: 30px;
  /*border-width: 1px;*/
  /*border-radius: 5px;*/
  /*border-style: double;*/
}
</style>