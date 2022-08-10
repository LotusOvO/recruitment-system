import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap'
import axios from '@/http'
import VueToasted from 'vue-toasted'

Vue.config.productionTip = false
Vue.prototype.$axios = axios

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

Vue.use(VueToasted,{
  theme: 'toasted-primary',
  position:'bottom-right',
  duration:3000,
  action:{
    text: '关闭',
    onClick:(e, toastObject) =>{
      toastObject.goAway(0);
    }
  },
});
