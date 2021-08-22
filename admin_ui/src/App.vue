<template>
    <div
        :class="{ dark_mode: darkMode, light_mode: !darkMode }"
        id="app"
    >
        <router-view />
        <MessagePopup />
        <AboutModal v-if="showAboutModal" />
    </div>
</template>


<script lang="ts">
import axios from "axios"
import * as i from "./interfaces"

import AboutModal from "./components/AboutModal.vue"
import MessagePopup from "./components/MessagePopup.vue"

export default {
    components: {
        AboutModal,
        MessagePopup,
    },
    computed: {
        darkMode() {
            return this.$store.state.darkMode
        },
        showAboutModal() {
            return this.$store.state.aboutModalModule.showAboutModal
        },
    },
    async created() {
        let darkMode = JSON.parse(localStorage.getItem("darkMode"))

        if (darkMode === null) {
            darkMode = false
        }

        this.$store.commit("updateDarkMode", darkMode)

        await this.$store.dispatch("fetchMeta")
    },
    async beforeCreate() {
        let app = this

        // Handle auth errors - redirect to login.
        axios.interceptors.response.use(
            function (response) {
                return response
            },
            function (error) {
                if (error.response && error.response.status == 401) {
                    console.log("Login required")
                    setTimeout(function () {
                        app.$router.push({
                            name: "login",
                        })
                    }, 0)
                }
                return Promise.reject(error)
            }
        )

        // Handle 405 errors - we get these when running the admin in
        // read only mode. Just show a message to the user.
        axios.interceptors.response.use(
            function (response) {
                return response
            },
            function (error) {
                if (error.response && error.response.status == 405) {
                    console.log("Method not allowed")
                    let message: i.APIResponseMessage = {
                        contents:
                            "Method not supported - running in read only mode.",
                        type: "error",
                    }
                    app.$store.commit("updateApiResponseMessage", message)
                }
                return Promise.reject(error)
            }
        )

        // Handle 404 errors - if a page isn't found.
        axios.interceptors.response.use(
            function (response) {
                return response
            },
            function (error) {
                if (error.response && error.response.status == 404) {
                    console.log("Page not found")
                    alert("Page not found")
                    app.$router.push({ name: "home" })
                }
                return Promise.reject(error)
            }
        )

        // Handle 502 errors - if the server can't be reached.
        axios.interceptors.response.use(
            function (response) {
                return response
            },
            function (error) {
                if (error.response && error.response.status == 502) {
                    console.log("The server can't be reached.")
                    let message: i.APIResponseMessage = {
                        contents:
                            "The server can't be reached - please try later.",
                        type: "error",
                    }
                    app.$store.commit("updateApiResponseMessage", message)
                }
                return Promise.reject(error)
            }
        )

        await this.$store.dispatch("fetchUser")
    },
}
</script>


<style lang="less">
@import "./main.less";
</style>
