import Vue from 'vue'
import VueRouter from 'vue-router'
import TestWord from "@/components/TestWord"
import LoginPage from "@/components/Login";
import RegisterPage from "@/components/Register";
import PositionsPage from "@/components/Positions";
import positionDetail from "@/components/PositionDetail";
import UserInfo from "@/components/UserInfo";
import RecruitInfo from "@/components/RecruitInfo";
import ManagePage from "@/components/ManagePage";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'test',
        component: TestWord
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterPage
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage
    },

    {
        path: '/recruitment/:position_id',
        name: 'positionDetail',
        component: positionDetail
    },
    {
        path: '/recruitment',
        name: 'recruitment',
        component: PositionsPage
    },
    {
        path: '/userinfo/:user_id',
        name: 'userinfo',
        component: UserInfo
    },
    {
        path: '/my_recruitment/:user_id',
        name: 'my_recruitment',
        component: RecruitInfo
    },
    {
        path: 'manage/:user_id',
        name: 'manage',
        component: ManagePage
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
  const token = window.localStorage.getItem('recsys-user-token')
  if (to.matched.some(record => record.meta.requiresAuth) && (!token)) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (token && to.name === 'login') {
    // 用户已登录，但又去访问登录页面时不让他过去
    next({
      path: from.fullPath
    })
  } else if (to.matched.length === 0) {  // 要前往的路由不存在时
    console.log('here')
    console.log(to.matched)
    // Vue.toasted.error('404: NOT FOUND', { icon: 'fingerprint' })
    if (from.name) {
      next({
        name: from.name
      })
    } else {
      next({
        path: '/'
      })
    }
  } else {
    next()
  }
})

export default router
