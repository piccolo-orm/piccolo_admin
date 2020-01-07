<template>
    <div id="login">
        <h1>Login</h1>
        <form v-on:submit.prevent="login">
            <label>Username</label>
            <input
                type="text"
                v-model="username"
            />

            <label>Password</label>
            <input
                type="password"
                v-model="password"
            />

            <button>Login</button>
        </form>
    </div>
</template>


<script>
import axios from "axios"

export default {
    data: function() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        async login() {
            console.log("Logging in")
            try {
                let response = await axios.post(`./api/login/`, {
                    username: this.username,
                    password: this.password
                })
            } catch (error) {
                console.log("Request failed")
                console.log(error.response)
                this.$store.commit("updateApiResponseMessage", {
                    contents: "Problem logging in",
                    type: "error"
                })
                return
            }
            let response = await axios.get("./api/user/")
            this.$store.commit("updateUser", response.data)

            let nextURL = this.$route.query.nextURL
            if (nextURL) {
                this.$router.push({ path: nextURL })
            } else {
                this.$router.push({ name: "home" })
            }
        }
    }
}
</script>


<style lang="less">
div#login {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    h1 {
        margin-top: 0;
        padding-top: 2rem;
    }
}
</style>
