<template>
    <div id="app">
        <router-view />
        <MessagePopup />
    </div>
</template>


<script>
import axios from 'axios'
import MessagePopup from "./components/MessagePopup.vue"

export default {
    components: {
        MessagePopup
    },
    async beforeCreate() {
        try {
            const response = await axios.get('./user/')
            this.$store.commit('updateUser', response.data)
        } catch (error) {
            if (error.response.status == 401) {
                console.log('Login required')
                this.$router.push({'name': 'login'})
            }
        }
    }
}
</script>


<style lang="less">
@purple: #4d0d58;
@dark_grey: #2d2d2d;
@light_blue: #009dff;

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
    label {
        display: block;
        padding-bottom: 0.2rem;
        padding-top: 0.8rem;
    }

    input {
        border: 1px solid rgba(255, 255, 255, 0.2);
        background-color: rgba(0, 0, 0, 0.1);
        box-sizing: border-box;
        padding: 0.5rem;
        color: white;
    }

    input,
    button {
        width: 100%;
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
