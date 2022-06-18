<template>
    <div id="change_password">
        <div class="inner">
            <BackButton />
            <h1>Create user</h1>
            <form v-on:submit.prevent="createNewUser">
                <label>Username</label>
                <input name="username" type="text" v-model="username" />

                <label>Email</label>
                <input name="email" type="text" v-model="email" />

                <label>Password</label>
                <input name="password" type="password" v-model="password" />

                <label>Password confirmation</label>
                <input
                    name="confirm_password"
                    type="password"
                    v-model="confirmPassword"
                />

                <button>Create user</button>
            </form>
        </div>
    </div>
</template>


<script>
import axios from "axios"
import BackButton from "../components/BackButton.vue"

export default {
    data() {
        return {
            username: "",
            email: "",
            password: "",
            confirmPassword: ""
        }
    },
    components: {
        BackButton
    },
    methods: {
        async createNewUser() {
            console.log("Creating new user")
            const payload = {
                username: this.username,
                email: this.email,
                password: this.password,
                confirm_password: this.confirmPassword
            }
            try {
                await axios.post(`./api/register/`, payload)
                this.$store.commit("updateApiResponseMessage", {
                    contents: "Successfully create a new user.",
                    type: "success"
                })
                setTimeout(() => {
                    this.$router.push({ name: "home" })
                }, 3000)
            } catch (error) {
                console.log("Request failed")
                console.log(error.response)
                this.$store.commit("updateApiResponseMessage", {
                    contents: "The form has errors. Creating user canceled.",
                    type: "error"
                })
                setTimeout(() => {
                    this.$router.push({ name: "createNewUser" })
                }, 5)
                return
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
