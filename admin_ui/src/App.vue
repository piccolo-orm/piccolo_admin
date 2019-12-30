<template>
    <div id="app">
        <router-view />
        <MessagePopup />
    </div>
</template>


<script>
import axios from "axios"
import MessagePopup from "./components/MessagePopup.vue"

export default {
    components: {
        MessagePopup
    },
    async beforeCreate() {
        let app = this

        axios.interceptors.response.use(
            function(response) {
                return response
            },
            function(error) {
                if (error.response && error.response.status == 401) {
                    console.log("Login required")
                    let nextURL = app.$route.path
                    if (nextURL !== "/login") {
                        setTimeout(function() {
                            app.$router.push({
                                name: "login",
                                query: {
                                    nextURL: nextURL
                                }
                            }),
                                0
                        })
                    }
                }
                return Promise.reject(error)
            }
        )

        const response = await axios.get("./api/user/")
        this.$store.commit("updateUser", response.data)
    }
}
</script>


<style lang="less">
@import "./vars.less";

html {
    height: 100%;
}

body {
    background-color: @dark_grey;
    height: 100%;
    margin: 0;
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: rgba(255, 255, 255, 0.8);
}

#app {
    height: 100%;

    label {
        display: block;
        padding-bottom: 0.2rem;
        padding-top: 0.5rem;
    }

    input,
    select {
        border: 1px solid rgba(255, 255, 255, 0.2);
        background-color: rgba(0, 0, 0, 0.1);
        box-sizing: border-box;
        padding: 0.5rem;
        color: white;
        margin-bottom: 0.5rem;
    }

    input,
    button,
    select {
        width: 100%;
    }

    select {
        appearance: none;
        -webkit-appearance: none;
        background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
        background-repeat: no-repeat, repeat;
        background-position: right 0.7em top 50%, 0 0;
        background-size: 0.65em auto, 100%;
    }

    button {
        background-color: @light_blue;
        color: white;
        border: none;
        padding: 1rem 1.5rem;
        text-transform: uppercase;
        font-size: 0.8rem;
        font-weight: bolder;
        margin-top: 1rem;

        &:hover {
            background-color: lighten(@light_blue, 10%);
        }
    }

    svg {
        padding-right: 0.3rem;
    }
}

a {
    color: rgba(255, 255, 255, 0.8);
}
</style>
