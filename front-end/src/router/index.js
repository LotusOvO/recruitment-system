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
        name: 'home',
        component: TestWord,
        meta:{
            title:'首页'
        }
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterPage,
        meta:{
            title:'注册'
        }
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage,
        meta:{
            title:'登录'
        }
    },

    {
        path: '/recruitment/:position_id',
        name: 'positionDetail',
        component: positionDetail,
        meta:{
            title:'岗位详情'
        }
    },
    {
        path: '/recruitment',
        name: 'recruitment',
        component: PositionsPage,
        meta:{
            title:'岗位信息'
        }
    },
    {
        path: '/userinfo/:user_id',
        name: 'userinfo',
        component: UserInfo,
        meta:{
            title:'个人资料'
        }
    },
    {
        path: '/my_recruitment/:user_id',
        name: 'my_recruitment',
        component: RecruitInfo,
        meta:{
            title:'应聘记录'
        }
    },
    {
        path: '/manage/:user_id',
        name: 'manage',
        component: ManagePage,
        meta:{
            title:'管理页面'
        }
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    const token = window.localStorage.getItem('recsys-user-token')
    document.querySelector('body').setAttribute('style', 'background-color: #f9f9f9');
    if(to.meta.title){
        document.title = to.meta.title
    }
    if (to.matched.some(record => record.meta.requiresAuth) && (!token)) {
        next({
            path: '/login',
            query: {redirect: to.fullPath}
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
