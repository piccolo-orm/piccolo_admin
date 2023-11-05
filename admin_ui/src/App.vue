<template>
    <div :class="{ dark_mode: darkMode, light_mode: !darkMode }" id="app">
        <router-view />
        <MessagePopup />
        <AboutModal v-if="showAboutModal" @close="hideAboutModal" />
        <TimezoneModal v-if="showTimezoneModal" @close="hideTimezoneModal" />
    </div>
</template>

<script lang="ts">
import axios from "axios"
import { defineComponent } from "vue"
import type * as i from "./interfaces"

import AboutModal from "./components/AboutModal.vue"
import MessagePopup from "./components/MessagePopup.vue"
import TimezoneModal from "./components/TimezoneModal.vue"

export default defineComponent({
    components: {
        AboutModal,
        MessagePopup,
        TimezoneModal
    },
    computed: {
        darkMode() {
            return this.$store.state.darkMode
        },
        showAboutModal() {
            return this.$store.state.aboutModalModule.showAboutModal
        },
        showTimezoneModal() {
            return this.$store.state.timezoneModalModule.showTimezoneModal
        },
        siteName() {
            return this.$store.state.metaModule.siteName
        }
    },
    methods: {
        hideAboutModal() {
            this.$store.commit("updateShowAboutModal", false)
        },
        hideTimezoneModal() {
            this.$store.commit("updateShowTimezoneModal", false)
        }
    },
    async created() {
        let darkMode = JSON.parse(localStorage.getItem("darkMode") ?? "false")

        if (darkMode === null) {
            darkMode = false
        }

        this.$store.commit("updateDarkMode", darkMode)

        await this.$store.dispatch("fetchMeta")
        document.title = this.siteName
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
                    const currentPath = app.$route.path

                    // If we're already on the login page, don't do anything
                    if (!currentPath.startsWith("/login")) {
                        console.log("Login required")

                        // We want to redirect back to the current page after
                        // logging in again, so we let the login page know
                        // about this via the `nextURL` query param.
                        setTimeout(function () {
                            app.$router.push({
                                name: "login",
                                query: {
                                    nextURL: currentPath
                                }
                            })
                        }, 0)
                    }
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
                        type: "error"
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
                        type: "error"
                    }
                    app.$store.commit("updateApiResponseMessage", message)
                }
                return Promise.reject(error)
            }
        )

        await this.$store.dispatch("setupTranslations")
        await this.$store.dispatch("fetchUser")
    }
})
</script>

<style lang="less">
@import "./main.less";
</style>
