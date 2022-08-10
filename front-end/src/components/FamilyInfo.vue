<template>
  <div>
    <div v-if="family.length > 0">
      <div class="work-card" v-for="item in family" :key="item.id">
        <form class="row g-3" @reset="setFamilyInfo(item.id)" @submit.prevent="deleteFamilyInfo(item.id)">
          <div class="col-md-6">
            <label for="name" class="form-label">亲属姓名</label>
            <input v-model="item.name" type="text" class="form-control" id="name">
          </div>
          <div class="col-md-6">
            <label for="phone_number" class="form-label">联系电话</label>
            <input v-model="item.phone_number" type="text" class="form-control" id="phone_number">
          </div>
          <div class="col-md-6">
            <label for="work" class="form-label">亲属工作</label>
            <input v-model="item.work" type="text" class="form-control" id="work">
          </div>
          <div class="col-md-6">
            <label for="relation" class="form-label">与本人关系</label>
            <input v-model="item.relation" type="text" class="form-control" id="relation">
          </div>
          <button type="reset" class="btn btn-warning col-md-2 container save-btn">保存修改</button>
          <button type="submit" class="btn btn-danger col-md-2 container save-btn">删除</button>
        </form>
      </div>
    </div>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary add-btn" data-bs-toggle="modal" data-bs-target="#staticBackdrop1">
      新增亲属
    </button>
    <!-- Modal -->
    <div class="modal fade" id="staticBackdrop1" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">新增亲属</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="row g-3">
              <div class="col-md-6">
                <label for="name" class="form-label">亲属姓名</label>
                <input v-model="familyForm.name" type="text" class="form-control" id="name">
              </div>
              <div class="col-md-6">
                <label for="phone_number" class="form-label">联系电话</label>
                <input v-model="familyForm.phone_number" type="text" class="form-control" id="phone_number">
              </div>
              <div class="col-md-6">
                <label for="work" class="form-label">亲属工作</label>
                <input v-model="familyForm.work" type="text" class="form-control" id="work">
              </div>
              <div class="col-md-6">
                <label for="relation" class="form-label">与本人关系</label>
                <input v-model="familyForm.relation" type="text" class="form-control" id="relation">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" v-on:click="addFamilyInfo">添加</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FamilyInfo",
  data() {
    return {
      family: [],
      familyForm: {
        name: '',
        phone_number: '',
        work: '',
        relation: '',
        errors: 0,
        errorInfo: []
      }
    }
  },
  methods: {
    getFamilyInfo(user_id) {
      const path = '/fam_info/' + user_id;
      this.$axios.get(path)
          .then((response) => {
            this.family = response.data;
          })
          .catch((error) => {
            console.log(error);
          })
    },
    setFamilyInfo(family_id) {
      const path = '/fam_info/' + this.$route.params.user_id;
      for (let i = 0; i < this.family.length; i++) {
        if (this.family[i].id === family_id) {
          this.$axios.put(path, this.family[i])
              .then((response) => {
                this.$toasted.success('保存完成')
                this.family = response.data;
              })
              .catch((error) => {
                this.$toasted.error('保存失败')
                console.log(error)
              })
          break;
        }
      }
    },
    deleteFamilyInfo(family_id) {
      const path = '/fam_info/' + this.$route.params.user_id;
      this.$axios.delete(path, {data: {id: family_id}})
          .then((response) => {
            this.$toasted.success('删除完成')
            this.family = response.data;
          })
          .catch((error) => {
            this.$toasted.error('删除失败')
            console.log(error);
          })
    },
    addFamilyInfo() {
      const path = '/fam_info/' + this.$route.params.user_id;
      if (this.familyForm.name === '') {
        this.familyForm.errors++;
        this.familyForm.errorInfo += "请填写姓名"
      }
      if (this.familyForm.phone_number === '') {
        this.familyForm.errors++;
        this.familyForm.errorInfo += "请填写联系电话"
      }
      if (this.familyForm.work === '') {
        this.familyForm.errors++;
        this.familyForm.errorInfo += "请填写工作"
      }
      if (this.familyForm.relation === '') {
        this.familyForm.errors++;
        this.familyForm.errorInfo += "请填写与本人关系"
      }
      console.log(this.familyForm.errors)
      if (this.familyForm.errors === 0) {
        this.$axios.post(path, {
          name: this.familyForm.name,
          phone_number: this.familyForm.phone_number,
          work: this.familyForm.work,
          relation: this.familyForm.relation
        })
            .then((response) => {
              this.$toasted.success('新增完成')
              this.family = response.data;
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
    this.getFamilyInfo(user_id);
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