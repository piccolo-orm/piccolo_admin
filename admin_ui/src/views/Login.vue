<template>
    <div id="login">
        <div class="inner">
            <h1>{{ siteName }}</h1>
            <form v-on:submit.prevent="login">
                <label>Username</label>
                <input
                    name="username"
                    type="text"
                    v-model="username"
                />

                <label>Password</label>
                <input
                    name="password"
                    type="password"
                    v-model="password"
                />

                <button>Login</button>
            </form>
        </div>
    </div>
</template>


<script>
import axios from "axios"

export default {
    data: function () {
        return {
            username: "",
            password: "",
        }
    },
    computed: {
        siteName() {
            return this.$store.state.siteName
        },
    },
    methods: {
        async login() {
            console.log("Logging in")
            try {
                await axios.post(`./auth/login/`, {
                    username: this.username,
                    password: this.password,
                })
                this.$router.push({ name: "home" })
            } catch (error) {
                console.log("Request failed")
                console.log(error.response)
                this.$store.commit("updateApiResponseMessage", {
                    contents: "Problem logging in",
                    type: "error",
                })
                return
            }

            await Promise.all([
                this.$store.dispatch("fetchUser"),
                this.$store.dispatch("fetchMeta"),
            ])
        },
    },
}
</script>


<style lang="less">
div#login {
    div.inner {
        margin: 0 auto;
        max-width: 30rem;
        padding: 0 0.5rem;

        h1 {
            margin-top: 0;
            padding-top: 4rem;
            text-align: center;
        }
    }
}
</style>
