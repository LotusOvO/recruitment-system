<template>
  <nav class="navbar navbar-light container">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">首页</router-link>
      <router-link to="/recruitment" class="navbar-brand">岗位</router-link>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="搜索热门岗位" aria-label="Search" v-model="searchText">
        <router-link class="btn btn-outline-success text-nowrap" type="submit" :to="{path:'/recruitment', query:{name : searchText}}">搜索</router-link>
      </form>
      <div v-if="sharedState.is_authenticated" class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" id="navbarDropdown" role="button" data-bs-toggle="dropdown"
           aria-expanded="false">
          {{ sharedState.user_name }}
        </a>
        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
          <li>
            <router-link :to="{name:'userinfo', params:{user_id: sharedState.user_id}}" class="dropdown-item">个人信息</router-link>
          </li>
          <li>
            <router-link :to="{name:'my_recruitment', params: {user_id: sharedState.user_id}}" class="dropdown-item">招聘进度</router-link>
          </li>
          <li v-if="sharedState.user_role === 1">
            <router-link :to="{name:'manage',params:{user_id:sharedState.user_id}}" class="dropdown-item">管理员界面</router-link>
          </li>
          <li>
            <hr class="dropdown-divider">
          </li>
          <li>
            <a v-on:click="logout" class="dropdown-item">注销</a>
          </li>
        </ul>
      </div>
      <div v-else class="nav-item">
        <router-link to="/login" class="nav-link">登录</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import store from "@/store";

export default {
  name: "NavBar",
  data() {
    return {
      sharedState: store.state,
      searchText:'',
    }
  },
  methods: {
    logout() {
      store.logoutAction();
      this.$router.replace({name: 'login'});
      this.$toasted.success('注销成功')
    }
  }
}
</script>

<style scoped>
.navbar {
  width: 70%;
  background-color: #e3f2fd;
  border-radius: 10px;
}
</style>