<template>
    <div id="login">
        <div class="inner">
            <div class="heading">
                <h1>{{ siteName }}</h1>
            </div>
            <form v-on:submit.prevent="login">
                <label>{{ $t("Username") }}</label>
                <input name="username" type="text" v-model="username" />

                <label>{{ $t("Password") }}</label>
                <PasswordInput v-model="password" />
                <button data-uitest="login_button">{{ $t("Login") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import PasswordInput from "../components/PasswordInput.vue"

export default {
    data() {
        return {
            username: "",
            password: ""
        }
    },
    components: {
        PasswordInput
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

        div.heading {
            text-align: center;

            h1 {
                margin-top: 0;
                padding-top: 4rem;
                text-align: center;
                border-bottom: 3px solid #009dff;
                display: inline-block;
            }
        }
    }
}
</style>
