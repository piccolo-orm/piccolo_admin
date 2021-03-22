<template>
    <div :class="{ dark_mode: darkMode, light_mode: !darkMode }" id="app">
        <router-view />
        <MessagePopup />
        <AboutModal v-if="showAboutModal" />
    </div>
</template>


<script lang="ts">
import axios from "axios"
import Vue from "vue"
import * as i from "./interfaces"

import AboutModal from "./components/AboutModal.vue"
import MessagePopup from "./components/MessagePopup.vue"

export default Vue.extend({
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
                    let nextURL = app.$route.path
                    if (nextURL !== "/login") {
                        setTimeout(function () {
                            app.$router.push({
                                name: "login",
                                query: {
                                    nextURL: nextURL,
                                },
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
})
</script>


<style lang="less">
@import "./vars.less";

html {
    height: 100%;
}

body {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    margin: 0;
    position: relative;
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

.light_mode {
    background-color: white;
    color: @dark_grey;

    .sidebar_wrapper,
    #sidebar_overlay {
        border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
    }

    div.sidebar {
        background-color: whitesmoke;

        li {
            a:hover {
                background-color: rgba(0, 0, 0, 0.03);
            }
        }
    }

    .right_column {
        border-left: 1px solid rgba(0, 0, 0, 0.1) !important;
    }

    ul#drop_down_menu {
        background-color: @dark_blue;
    }

    ul.pagination {
        li {
            a {
                &:hover {
                    background-color: whitesmoke;
                }

                &.active {
                    background-color: whitesmoke;
                }
            }
        }
    }

    a {
        color: @dark_blue;

        &:hover {
            color: lighten(@dark_blue, 10%);
        }

        &.subtle {
            color: @dark_grey;

            &:hover {
                color: @dark_grey;
            }
        }
    }

    input,
    select,
    textarea {
        background-color: darken(white, 5%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: @dark_grey;
    }

    tr {
        &:nth-child(even) {
            background-color: whitesmoke;
        }
    }

    .opaque {
        background-color: white;
    }

    #nav {
        background-color: @dark_blue;
    }

    button {
        background-color: @dark_blue;

        &:hover {
            background-color: lighten(@dark_blue, 10%);
        }
    }
}

.dark_mode {
    background-color: @dark_grey;
    color: @off_white;

    a {
        color: @light_blue;

        &:hover {
            color: lighten(@light_blue, 10%);
        }

        &.subtle {
            color: @off_white;

            &:hover {
                color: white;
            }
        }
    }

    ul#drop_down_menu {
        background-color: lighten(@dark_grey, 5%);
    }

    tr {
        &:nth-child(even) {
            background-color: darken(@dark_grey, 3%);
        }
    }

    input,
    select,
    textarea {
        background-color: darken(@dark_grey, 4%);
        border: 1px solid rgba(0, 0, 0, 0.2);
        color: @off_white;
    }

    .opaque {
        background-color: @dark_grey;
    }

    #nav {
        background-color: darken(@dark_grey, 5%);
    }

    button {
        background-color: @light_blue;

        &:hover {
            background-color: lighten(@light_blue, 10%);
        }
    }
}

#app {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    min-height: 100%;

    label {
        display: block;
        padding-bottom: 0.2rem;
        padding-top: 0.8rem;
    }

    input[type="text"],
    input[type="number"],
    input[type="password"],
    select,
    textarea {
        box-sizing: border-box;
        font-size: 0.8rem;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
    }

    input[type="text"],
    input[type="number"],
    input[type="password"],
    button,
    select,
    textarea {
        width: 100%;
    }

    textarea {
        min-height: 3rem;
        max-width: 100%;
        min-width: 100%;
    }

    select {
        appearance: none;
        -webkit-appearance: none;
        background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
        background-repeat: no-repeat, repeat;
        background-position: right 0.7em top 50%, 0 0;
        background-size: 0.65em auto, 100%;
        border-radius: 0;
    }

    button {
        color: white;
        border: none;
        padding: 0.8rem 1.2rem;
        text-transform: uppercase;
        font-size: 0.7rem;
        font-weight: bolder;
        margin-top: 1rem;
        transition: background-color 0.5s;

        &:hover {
            transition: background-color 0.5s;
        }
    }

    a {
        transition: color 0.5s;

        &:hover {
            transition: color 0.5s;
        }

        &.button {
            background-color: @dark_blue;
            color: white;
            font-size: 0.7em;
            padding: 0.3rem 0.5rem;
            text-transform: uppercase;
        }
    }

    svg {
        padding-right: 0.3rem;
    }
}
</style>
