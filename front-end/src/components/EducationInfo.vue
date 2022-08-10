<template>
  <div>
    <div v-if="education.length > 0">
      <div class="major-card" v-for="item in education" :key="item.id">
        <form class="row g-3" @reset="setEducationInfo(item.id)" @submit.prevent="deleteEducationInfo(item.id)">
          <div class="col-md-6">
            <label for="degree" class="form-label">学位</label>
            <input v-model="item.degree" type="text" class="form-control" id="degree">
          </div>
          <div class="col-md-6">
            <label for="school" class="form-label">学校</label>
            <input v-model="item.school" type="text" class="form-control" id="school">
          </div>
          <div class="col-md-6">
            <label for="major" class="form-label">专业</label>
            <input v-model="item.major" type="text" class="form-control" id="major">
          </div>
          <div class="col-md-6">
            <label for="begin_date" class="form-label">入学时间</label>
            <input v-model="item.begin_date" type="text" class="form-control" id="begin_date">
          </div>
          <div class="col-md-6">
            <label for="end_date" class="form-label">毕业时间</label>
            <input v-model="item.end_date" type="text" class="form-control" id="end_date">
          </div>
          <div class="col-md-6"></div>
          <button type="reset" class="btn btn-warning col-md-2 container save-btn">保存修改</button>
          <button type="submit" class="btn btn-danger col-md-2 container save-btn">删除</button>
        </form>
      </div>
    </div>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary add-btn" data-bs-toggle="modal" data-bs-target="#staticBackdrop2">
      新增学历
    </button>
    <!-- Modal -->
    <div class="modal fade" id="staticBackdrop2" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">新增学历</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="row g-3">
              <div class="col-md-6">
                <label for="degree" class="form-label">学位</label>
                <input v-model="educationForm.degree" type="text" class="form-control" id="degree">
              </div>
              <div class="col-md-6">
                <label for="school" class="form-label">学校</label>
                <input v-model="educationForm.school" type="text" class="form-control" id="school">
              </div>
              <div class="col-md-6">
                <label for="major" class="form-label">专业</label>
                <input v-model="educationForm.major" type="text" class="form-control" id="major">
              </div>
              <div class="col-md-6">
                <label for="begin_date" class="form-label">入学时间</label>
                <input v-model="educationForm.begin_date" type="text" class="form-control" id="begin_date">
              </div>
              <div class="col-md-6">
                <label for="end_date" class="form-label">毕业时间</label>
                <input v-model="educationForm.end_date" type="text" class="form-control" id="end_date">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" v-on:click="addEducationInfo">添加
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  degree: "EducationInfo",
  data() {
    return {
      education: [],
      educationForm: {
        degree: '',
        school: '',
        major: '',
        begin_date: '',
        end_date: '',
        errors: 0,
        errorInfo: []
      }
    }
  },
  methods: {
    getEducationInfo(user_id) {
      const path = '/edu_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.education = response.data;
          })
          .catch((error) => {
            console.log(error);
          })
    },
    setEducationInfo(education_id) {
      const path = '/edu_info/' + this.$route.params.user_id;
      for (let i = 0; i < this.education.length; i++) {
        if (this.education[i].id === education_id) {
          this.$axios.put(path, this.education[i])
              .then((response) => {
                this.$toasted.success('保存完成')
                this.education = response.data;
              })
              .catch((error) => {
                this.$toasted.error('保存失败')
                console.log(error)
              })
          break;
        }
      }
    },
    deleteEducationInfo(education_id) {
      const path = '/edu_info/' + this.$route.params.user_id;
      this.$axios.delete(path, {data: {id: education_id}})
          .then((response) => {
            this.$toasted.success('删除完成')
            this.education = response.data;
          })
          .catch((error) => {
            this.$toasted.error('删除失败')
            console.log(error);
          })
    },
    addEducationInfo() {
      const path = '/edu_info/' + this.$route.params.user_id;
      if (this.educationForm.degree === '') {
        this.educationForm.errors++;
        this.educationForm.errorInfo += "请填写学位"
      }
      if (this.educationForm.school === '') {
        this.educationForm.errors++;
        this.educationForm.errorInfo += "请填写学校"
      }
      if (this.educationForm.major === '') {
        this.educationForm.errors++;
        this.educationForm.errorInfo += "请填写学位"
      }
      if (this.educationForm.begin_date === '') {
        this.educationForm.errors++;
        this.educationForm.errorInfo += "请填写入学时间"
      }
      if (this.educationForm.end_date === '') {
        this.educationForm.errors++;
        this.educationForm.errorInfo += "请填写毕业时间"
      }
      console.log(this.educationForm.errors)
      if (this.educationForm.errors === 0) {
        this.$axios.post(path, {
          degree: this.educationForm.degree,
          school: this.educationForm.school,
          major: this.educationForm.major,
          begin_date: this.educationForm.begin_date,
          end_date: this.educationForm.end_date
        })
            .then((response) => {
              this.$toasted.success('新增完成')
              this.education = response.data;
            })
            .catch((error) => {
              this.$toasted.error('新增失败')
              console.log(error)
            })
      }
    }
  },
  created() {
    const user_id = this.$route.params.user_id;
    this.getEducationInfo(user_id);
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

.major-card {
  margin-bottom: 30px;
  /*border-width: 1px;*/
  /*border-radius: 5px;*/
  /*border-style: double;*/
}
</style>