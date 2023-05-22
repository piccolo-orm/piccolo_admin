<template>
    <div id="login">
        <div class="inner">
            <h1>{{ siteName }}</h1>
            <form v-on:submit.prevent="login">
                <label>{{ $t("Username") }}</label>
                <input name="username" type="text" v-model="username" />

                <label>{{ $t("Password") }}</label>
                <input
                    name="password"
                    v-model="password"
                    v-bind:type="showPassword ? 'text' : 'password'"
                />
                <span class="viewer" v-on:click="showPassword = !showPassword">
                    <font-awesome-icon v-if="!showPassword" icon="eye" />
                    <font-awesome-icon v-else icon="eye-slash" />
                </span>
                <button data-uitest="login_button">{{ $t("Login") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"

export default {
    data() {
        return {
            username: "",
            password: "",
            showPassword: false
        }
    },
    computed: {
        siteName() {
            return this.$store.state.metaModule.siteName
        }
    },
    methods: {
        async login() {
            console.log("Logging in")
            try {
                await axios.post(`./public/login/`, {
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

            await this.$store.dispatch("fetchUser")

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
    div.inner {
        margin: 0 auto;
        max-width: 30rem;
        padding: 0 0.5rem;

        h1 {
            margin-top: 0;
            padding-top: 4rem;
            text-align: center;
            text-underline-offset: 10px;
            text-decoration: underline 3px solid #009dff;
        }

        .viewer {
            float: right;
            margin-top: -2.1rem;
            margin-right: 0.4rem;
            position: relative;
            z-index: 1;
            cursor: pointer;
        }
    }
}
</style>
