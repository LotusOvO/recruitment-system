import Vue from 'vue'
import VueRouter from 'vue-router'
import TestWord from "@/components/TestWord"
import LoginPage from "@/components/Login";
import RegisterPage from "@/components/Register";

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
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
