<template>
  <div>
    <form class="row" @submit.prevent="searchPosition(searchForm.name,searchForm.location)">
      <div class="col-md-1"></div>
      <input v-model="searchForm.name" class="col-md-3 col-form-control" id="name" type="text" placeholder="岗位名称">
      <div class="col-md-1"></div>
      <input v-model="searchForm.location" class="col-md-3 col-form-control" id="location" type="text"
             placeholder="工作地点">
      <div class="col-md-1"></div>
      <button class="btn col-md-2 btn-primary" type="submit">搜索</button>
    </form>
    <div v-for="position in positions" v-bind:key="position.id">
      <br>
      <div class="card card2 container">
        <div class="card-body">
          <p class="card-text">岗位名称：{{ position.name }}</p>
          <p class="card-text">工作部门：{{ position.department }}</p>
          <p class="card-text">工作地点：{{ position.location }}</p>
          <div class="row">
            <div class="col-md-1"></div>
            <button class="btn btn-warning col-md-3" data-bs-toggle="modal" data-bs-target="#staticBackdrop0"
                    v-on:click="getPosition(position.id)">修改
            </button>
            <div class="col-md-4"></div>
            <button class="btn btn-danger col-md-3" v-on:click="deletePosition(position.id)">删除</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="staticBackdrop0" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">修改岗位</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="row g-3">
              <div class="col-md-6">
                <label for="name" class="form-label">岗位名称</label>
                <input v-model="positionForm.name" type="text" class="form-control" id="name">
              </div>
              <div class="col-md-6">
                <label for="department" class="form-label">工作部门</label>
                <input v-model="positionForm.department" type="text" class="form-control" id="department">
              </div>
              <div class="col-md-6">
                <label for="location" class="form-label">工作地点</label>
                <input v-model="positionForm.location" type="text" class="form-control" id="location">
              </div>
              <div class="col-md-12">
                <label for="requirement" class="form-label">岗位要求</label>
                <textarea v-model="positionForm.requirement" type="text" class="form-control"
                          id="requirement"></textarea>
              </div>
              <div class="col-md-12">
                <label for="describe" class="form-label">详细描述</label>
                <textarea v-model="positionForm.describe" type="text" class="form-control" id="describe"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" v-on:click="updatePosition(positionForm.id)">保存</button>
          </div>
        </div>
      </div>
    </div>

    <button type="button" class="btn btn-primary add-btn" data-bs-toggle="modal" data-bs-target="#staticBackdrop"
            style="margin-top: 15px;" v-on:click="clearForm">
      新增岗位
    </button>
    <!-- Modal -->
    <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
         aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">新增岗位</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form class="row g-3">
              <div class="col-md-6">
                <label for="name" class="form-label">岗位名称</label>
                <input v-model="positionForm.name" type="text" class="form-control" id="name">
              </div>
              <div class="col-md-6">
                <label for="department" class="form-label">工作部门</label>
                <input v-model="positionForm.department" type="text" class="form-control" id="department">
              </div>
              <div class="col-md-6">
                <label for="location" class="form-label">工作地点</label>
                <input v-model="positionForm.location" type="text" class="form-control" id="location">
              </div>
              <div class="col-md-12">
                <label for="requirement" class="form-label">岗位要求</label>
                <textarea v-model="positionForm.requirement" type="text" class="form-control"
                          id="requirement"></textarea>
              </div>
              <div class="col-md-12">
                <label for="describe" class="form-label">详细描述</label>
                <textarea v-model="positionForm.describe" type="text" class="form-control" id="describe"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" v-on:click="addPosition">添加</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "PositionManage",
  data() {
    return {
      positions: [],
      positionForm: {
        id: '',
        name: '',
        department: '',
        location: '',
        describe: '',
        requirement: '',
        errors: 0,
        errorInfo: [],
      },
      searchForm: {
        name: '',
        location: ''
      }
    }
  },
  methods: {
    searchPosition(name = '', location = '') {
      let path = '/recruitment/search'
      if (name !== '' && location !== '') {
        path += '?name=' + name + '&location=' + location;
      } else {
        if (location !== '') {
          path += '?location=' + location;
        }
        if (name !== '') {
          path += '?name=' + name;
        }
      }
      this.$axios.get(path)
          .then((response) => {
            this.positions = response.data
          })
          .catch((error) => {
            console.log(error)
          })
    },
    clearForm() {
      this.positionForm = {
        id: '',
        name: '',
        department: '',
        location: '',
        describe: '',
        requirement: '',
        errors: 0,
        errorInfo: [],
      }
    },
    addPosition() {
      const path = '/recruitment';
      if (this.positionForm.name === '') {
        this.positionForm.errors++;
      }
      if (this.positionForm.department === '') {
        this.positionForm.errors++;
      }
      if (this.positionForm.location === '') {
        this.positionForm.errors++;
      }
      if (this.positionForm.errors > 0) {
        this.positionForm.errors =0;
        return;
      }

      this.$axios.post(path, {
        name: this.positionForm.name,
        department: this.positionForm.department,
        location: this.positionForm.location,
        requirement: this.positionForm.requirement,
        describe: this.positionForm.describe
      })
          .then((response) => {
            this.$toasted.success('新增完成')
            this.positions = response.data;
          })
          .catch((error) => {
            this.$toasted.error('新增失败')
            console.log(error)
          })
      this.clearForm();
    },
    deletePosition(position_id) {
      const path = '/recruitment/' + position_id;
      this.$axios.delete(path)
          .then((response) => {
            this.$toasted.success('删除完成')
            this.positions = response.data;
          })
          .catch((error) => {
            this.$toasted.error('删除失败')
            console.log(error)
          })
    },
    getPosition(position_id) {
      const path = '/recruitment/' + position_id;
      this.$axios.get(path)
          .then((response) => {
            this.positionForm.id = response.data.id;
            this.positionForm.name = response.data.name;
            this.positionForm.department = response.data.department;
            this.positionForm.location = response.data.location;
            this.positionForm.describe = response.data.describe;
            this.positionForm.requirement = response.data.requirement;
          })
          .catch((error) => {
            console.log(error);
          })
    },
    updatePosition(position_id) {
      const path = '/recruitment/' + position_id;
      if (this.positionForm.name === '') {
        this.positionForm.errors++;
      }
      if (this.positionForm.department === '') {
        this.positionForm.errors++;
      }
      if (this.positionForm.location === '') {
        this.positionForm.errors++;
      }
      if (this.positionForm.errors > 0) {
        this.positionForm.errors =0;
        return;
      }

      this.$axios.put(path, {
        id: this.positionForm.id,
        name: this.positionForm.name,
        department: this.positionForm.department,
        location: this.positionForm.location,
        requirement: this.positionForm.requirement,
        describe: this.positionForm.describe
      })
          .then(() => {
            this.$toasted.success('保存完成')
            this.searchPosition();
          })
          .catch((error) => {
            this.$toasted.error('保存失败')
            console.log(error);
          })
    }
  },
  created() {
    this.searchPosition()
  }
}
</script>

<style scoped>
.card2 {
  /*width: 50%;*/
  border-radius: 10px;
}
</style>