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
                <div class="password_wrapper">
                    <input
                        name="password"
                        v-model="password"
                        v-bind:type="showPassword ? 'text' : 'password'"
                    />
                    <span
                        class="viewer"
                        v-if="password"
                        v-on:click="showPassword = !showPassword"
                    >
                        <font-awesome-icon
                            v-if="!showPassword"
                            icon="eye"
                            title="Show password"
                        />
                        <font-awesome-icon
                            v-else
                            icon="eye-slash"
                            title="Hide password"
                        />
                    </span>
                </div>
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

        div.password_wrapper {
            position: relative;

            span.viewer {
                color: #878787;
                position: absolute;
                top: 0.5rem;
                right: 0.5rem;
                z-index: 1;
                cursor: pointer;
            }
        }
    }
}
</style>
