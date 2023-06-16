<template>
    <div id="change_password">
        <div class="inner">
            <BackButton />
            <div class="heading">
                <h1>{{ $t("Change password") }}</h1>
            </div>
            <form v-on:submit.prevent="changePassword">
                <label>{{ $t("Current password") }}</label>
                <Password
                    v-model="currentPassword"
                    v-on:input="passwordValue"
                />
                <label>{{ $t("New password") }}</label>
                <Password v-model="newPassword" v-on:input="passwordValue" />
                <label>{{ $t("New password confirmation") }}</label>
                <Password
                    v-model="confirmNewPassword"
                    v-on:input="passwordValue"
                />
                <button>{{ $t("Change password") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import BackButton from "../components/BackButton.vue"
import Password from "../components/Password.vue"

export default {
    data() {
        return {
            currentPassword: "",
            newPassword: "",
            confirmNewPassword: ""
        }
    },
    components: {
        BackButton,
        Password
    },
    methods: {
        async changePassword() {
            const payload = {
                current_password: this.currentPassword,
                new_password: this.newPassword,
                confirm_new_password: this.confirmNewPassword
            }
            try {
                await axios.post(`./api/change-password/`, payload)
                this.$store.commit("updateApiResponseMessage", {
                    contents: `Changed password successfully. You will be redirected
                        to log in with your new credentials.`,
                    type: "success"
                })
                setTimeout(() => {
                    this.$router.push({ name: "home" })
                }, 3000)
            } catch (error) {
                console.log("Request failed")
                console.log(error.response)
                this.$store.commit("updateApiResponseMessage", {
                    contents: `Error - ${error.response.data.detail}`,
                    type: "error"
                })
            }
        }
    }
}
</script>

<style lang="less">
div#change_password {
    div.inner {
        margin: 0 auto;
        max-width: 30rem;
        padding: 2rem 2rem;

        h1 {
            margin-top: 0;
            padding-top: 0.5rem;
            text-align: center;
        }
    }
}
</style>
