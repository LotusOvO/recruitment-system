<template>
  <div>
    <br>
    <div class="d-flex align-items-start my_nav">
      <div class="nav flex-column nav-pills me-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
        <button class="nav-link active" id="v-pills-positions-tab" data-bs-toggle="pill"
                data-bs-target="#v-pills-positions"
                type="button" role="tab" aria-controls="v-pills-positions" aria-selected="true">岗位管理
        </button>
        <button class="nav-link" id="v-pills-recruitment-tab" data-bs-toggle="pill" data-bs-target="#v-pills-recruitment"
                type="button" role="tab" aria-controls="v-pills-recruitment" aria-selected="false">应聘管理
        </button>
      </div>
      <div class="tab-content" id="v-pills-tabContent">
        <div class="tab-pane fade show active" id="v-pills-positions" role="tabpanel"
             aria-labelledby="v-pills-positions-tab">
          <PositionManage></PositionManage>
        </div>
        <div class="tab-pane fade" id="v-pills-recruitment" role="tabpanel" aria-labelledby="v-pills-recruitment-tab">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PositionManage from "@/components/PositionManage";
export default {
  name: "ManagePage",
  components: {PositionManage},
}
</script>

<style scoped>
.my_nav {
  margin-left: 15%;
  margin-right: 15%;
}
.nav{
  border-style: solid;
  border-width: 2px;
  border-radius: 10px;
  border-color: #0d6efd;
  width: 60px;
}
.tab-content{
  width: 100%;
}
</style>