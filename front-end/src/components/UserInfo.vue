<template>
  <div>
    <br>
    <div class="d-flex align-items-start my_nav">
      <div class="nav flex-column nav-pills me-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
        <button class="nav-link active" id="v-pills-base-info-tab" data-bs-toggle="pill" data-bs-target="#v-pills-base-info"
                type="button" role="tab" aria-controls="v-pills-base-info" aria-selected="true">基本信息
        </button>
        <button class="nav-link" id="v-pills-work-info-tab" data-bs-toggle="pill" data-bs-target="#v-pills-work-info"
                type="button" role="tab" aria-controls="v-pills-work-info" aria-selected="false">工作经历
        </button>
        <button class="nav-link" id="v-pills-family-info-tab" data-bs-toggle="pill" data-bs-target="#v-pills-family-info"
                type="button" role="tab" aria-controls="v-pills-family-info" aria-selected="false">家庭信息
        </button>
        <button class="nav-link" id="v-pills-education-info-tab" data-bs-toggle="pill" data-bs-target="#v-pills-education-info"
                type="button" role="tab" aria-controls="v-pills-education-info" aria-selected="false">学历信息
        </button>
      </div>
      <div class="tab-content" id="v-pills-tabContent">
        <div class="tab-pane fade show active" id="v-pills-base-info" role="tabpanel" aria-labelledby="v-pills-base-info-tab">
          <BaseInfo></BaseInfo>
        </div>
        <div class="tab-pane fade" id="v-pills-work-info" role="tabpanel" aria-labelledby="v-pills-work-info-tab">
          <WorkInfo></WorkInfo>
        </div>
        <div class="tab-pane fade" id="v-pills-family-info" role="tabpanel" aria-labelledby="v-pills-family-info-tab">
          <FamilyInfo></FamilyInfo>
        </div>
        <div class="tab-pane fade" id="v-pills-education-info" role="tabpanel" aria-labelledby="v-pills-education-info-tab">
          <EducationInfo></EducationInfo>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseInfo from "@/components/BaseInfo";
import WorkInfo from "@/components/WorkInfo";
import FamilyInfo from "@/components/FamilyInfo";
import EducationInfo from "@/components/EducationInfo";

export default {
  name: "UserInfo",
  components:{
    EducationInfo,
    FamilyInfo,
    WorkInfo,
    BaseInfo,
  }
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
</style>