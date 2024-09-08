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
                <PasswordInput @input="password = $event" :value="password" />

                <template v-if="mfaCodeRequired">
                    <label>{{ $t("MFA Code") }}</label>
                    <input placeholder="123456" type="text" v-model="mfaCode" />
                    <p>
                        Hint: Use your authenticator app to generate the MFA
                        code - if you've lost your phone, you can use a recovery
                        code instead.
                    </p>
                </template>

                <button data-uitest="login_button">{{ $t("Login") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import axios from "axios"
import PasswordInput from "../components/PasswordInput.vue"

export default defineComponent({
    data() {
        return {
            username: "",
            password: "",
            mfaCode: "",
            mfaCodeRequired: false
        }
    },
    components: {
        PasswordInput
    },
    computed: {
        siteName(): string {
            return this.$store.state.metaModule.siteName
        }
    },
    methods: {
        async login() {
            console.log("Logging in")
            try {
                await axios.post(`./public/login/`, {
                    username: this.username,
                    password: this.password,
                    ...(this.mfaCodeRequired ? { mfa_code: this.mfaCode } : {})
                })
            } catch (error) {
                console.log("Request failed")

                if (axios.isAxiosError(error)) {
                    console.log(error.response)

                    if (
                        error.response?.status == 401 &&
                        error.response?.data?.detail == "MFA code required"
                    ) {
                        this.$store.commit("updateApiResponseMessage", {
                            contents: "MFA code required",
                            type: "neutral"
                        })

                        this.mfaCodeRequired = true
                    } else {
                        this.$store.commit("updateApiResponseMessage", {
                            contents: "Problem logging in",
                            type: "error"
                        })
                    }
                }

                return
            }

            await this.$store.dispatch("fetchUser")

            let nextURL = this.$route.query.nextURL as string

            if (nextURL && !nextURL.startsWith("/login")) {
                await this.$router.push({ path: nextURL })
            } else {
                await this.$router.push({ name: "home" })
            }
        }
    }
})
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
