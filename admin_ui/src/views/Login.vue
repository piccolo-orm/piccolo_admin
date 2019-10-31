<template>
<div id="login">
    <h1>Login</h1>
    <form v-on:submit.prevent="login">
        <label>Username</label>
        <input type="text" v-model="username">

        <label>Password</label>
        <input type="password" v-model="password">

        <button>Login</button>
    </form>
</div>
</template>


<script>
import axios from 'axios'

const BASE_URL = process.env.VUE_APP_BASE_URI

export default {
    data: function() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        async login() {
            console.log("Logging in")
            let response = await axios.post(`${BASE_URL}login/`, {username: this.username, password: this.password})
            this.$router.push({name: 'home'})
        }
    }
}
</script>


<style lang="less">
div#login {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;
}
</style>
