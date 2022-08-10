<template>
  <div class="container">
    <h1>注册</h1>
    <div class="row">
      <div class="col-md-4 container">
        <form @submit.prevent="onSubmit">
          <div class="form-group">
            <label for="email">邮箱</label>
            <input type="email" v-model="registerForm.email" class="form-control" v-bind:class="{'is-invalid': registerForm.emailError}" id="email" aria-describedby="emailHelp" placeholder="">
            <div v-show="registerForm.emailError" class="invalid-feedback">{{ registerForm.emailError }}</div>
          </div>
          <br>
          <div class="form-group">
            <label for="password">密码</label>
            <input type="password" v-model="registerForm.password" class="form-control" v-bind:class="{'is-invalid': registerForm.passwordError}" id="password" placeholder="">
            <div v-show="registerForm.passwordError" class="invalid-feedback">{{ registerForm.passwordError }}</div>
          </div>
          <br>
          <div class="form-group">
            <label for="re_password">重复密码</label>
            <input type="password" v-model="registerForm.re_password" class="form-control" v-bind:class="{'is-invalid': registerForm.passwordError}" id="re_password" placeholder="">
          </div>
          <br>
          <button type="submit" class="btn btn-primary">注册</button>
        </form>
      </div>
    </div>
    <br>
    <p>已有账号？
      <router-link to="/login">前往登录</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: "RegisterPage",
  data() {
    return {
      registerForm: {
        email: '',
        password: '',
        re_password: '',
        submitted: '',
        errors: 0,
        emailError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit() {
      this.registerForm.submitted = true  // 先更新状态
      this.registerForm.errors = 0

      if (!this.registerForm.email) {
        this.registerForm.errors++
        this.registerForm.emailError = '请输入邮箱'
      } else {
        this.registerForm.emailError = null
      }
      if (!this.registerForm.password) {
        this.registerForm.errors++
        this.registerForm.passwordError = '请输入密码'
      } else {
        this.registerForm.passwordError = null
      }
      if (!this.registerForm.re_password) {
        this.registerForm.errors++
        this.registerForm.passwordError = '请再次输入密码'
      } else if (this.registerForm.password !== this.registerForm.re_password) {
        this.registerForm.errors++
        this.registerForm.passwordError = '两次密码不一致'
      } else {
        this.registerForm.passwordError = null
      }

      if (this.registerForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/users'
      const payload = {
        email: this.registerForm.email,
        password: this.registerForm.password
      }
      this.$axios.post(path, payload)
          .then(() => {
            this.$router.push('/login')
            this.$toasted.success('注册成功')
          })
          .catch((error) => {
            if ('email' in error.response.data.message) {
              this.registerForm.emailError = error.response.data.message.email
            }
            if ('password' in error.response.data.message) {
              this.registerForm.emailError = error.response.data.message.password
            }
            this.$toasted.error('注册失败')
      })
    }
  }
}
</script>

<style scoped>

</style>