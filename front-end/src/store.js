export default {
    debug: true,
    state: {
        is_authenticated: window.localStorage.getItem('recsys-user-token') ? true : false,
        user_id: window.localStorage.getItem('recsys-user-token') ?
            JSON.parse(atob(window.localStorage.getItem('recsys-user-token').split('.')[1])).user_id
            : 0
    },
    loginAction() {
        if (this.debug) {
            console.log('loginAction triggered')
        }
        console.log(this.state.user_id)
        this.state.is_authenticated = true
        this.state.user_id = JSON.parse(atob(window.localStorage.getItem('recsys-user-token').split('.')[1])).user_id
    },
    logoutAction() {
        if (this.debug) console.log('logoutAction triggered')
        window.localStorage.removeItem('recsys-user-token')
        this.state.is_authenticated = false
        this.state.user_id = 0
    }
}