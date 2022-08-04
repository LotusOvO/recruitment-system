<template>
  <div class="container">
    <h1>登录</h1>
    <div class="row">
      <div class="col-md-4 container">
        <form @submit.prevent="onSubmit">
          <div class="form-group">
            <label for="email">邮箱</label>
            <input type="text" v-model="loginForm.email" class="form-control"
                   v-bind:class="{'is-invalid': loginForm.emailError}" id="username" aria-describedby="emailHelp" placeholder="">
            <div v-show="loginForm.usernameError" class="invalid-feedback">{{ loginForm.emailError }}</div>
          </div>
          <br>
          <div class="form-group">
            <label for="password">密码</label>
            <input type="password" v-model="loginForm.password" class="form-control"
                   v-bind:class="{'is-invalid': loginForm.passwordError}" id="password" placeholder="">
            <div v-show="loginForm.passwordError" class="invalid-feedback">{{ loginForm.passwordError }}</div>
          </div>
          <br>
          <button type="submit" class="btn btn-primary">登录</button>
        </form>
      </div>
    </div>
    <br>
    <p>没有账号？
      <router-link to="/register">前往注册</router-link>
    </p>
<!--    <p>-->
<!--      Forgot Your Password?-->
<!--      <a href="#">Click to Reset It</a>-->
<!--    </p>-->
  </div>
</template>

<script>
import store from "@/store";

export default {
  name: "LoginPage",
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
        submitted: false,
        errors: 0,
        emailError: '',
        passwordError: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.loginForm.submitted = true;
      this.loginForm.errors = 0;

      if (!this.loginForm.email) {
        this.loginForm.errors++;
        this.loginForm.emailError = '请输入邮箱';
      } else if (!this.validEmail(this.loginForm.email)) {
        this.loginForm.errors++;
        this.loginForm.emailError = '请输入有效邮箱';
      } else {
        this.loginForm.emailError = null;
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++;
        this.loginForm.passwordError = '请输入密码';
      } else {
        this.loginForm.passwordError = null;
      }

      if (this.loginForm.errors > 0) {
        return false;
      }

      const path = '/tokens';
      this.$axios.post(path, {}, {
        auth: {
          'username': this.loginForm.email,
          'password': this.loginForm.password
        }
      }).then((response) => {
        window.localStorage.setItem('recsys-user-token', response.data.token)
        store.loginAction()

      }).catch((error) => {
        // handle error
        console.log(error)
        if (error) {
          if (error.response.status === 401) {
            this.loginForm.usernameError = '邮箱或密码错误'
            this.loginForm.passwordError = '邮箱或密码错误'
          }
          else {
            console.log(error.response)
          }
        }
      })

    },
    validEmail: function (email) {
      // const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}])|(([a-zA-Z\-\d]+\.)+[a-zA-Z]{2,}))$/;
      // return re.test(email);
      if (email)
        return true;
    }
  }
}
</script>

<style scoped>

</style>