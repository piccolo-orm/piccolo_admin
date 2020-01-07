<template>
    <ul id="drop_down_menu">
        <li v-if="darkMode">
            <a
                href="#"
                v-on:click.prevent="updateDarkMode(false)"
            >
                <font-awesome-icon icon="sun" />Light Mode
            </a>
        </li>
        <li v-else>
            <a
                href="#"
                v-on:click.prevent="updateDarkMode(true)"
            >
                <font-awesome-icon icon="moon" />Dark Mode
            </a>
        </li>
        <li>
            <a
                href="#"
                v-on:click.prevent="logout"
            >
                <font-awesome-icon icon="sign-out-alt" />Log out
            </a>
        </li>
    </ul>
</template>

<script lang="ts">
import axios from "axios"
import Vue from "vue"

export default Vue.extend({
    computed: {
        darkMode() {
            return this.$store.state.darkMode
        }
    },
    methods: {
        updateDarkMode(enabled: boolean) {
            this.$store.commit("updateDarkMode", enabled)
        },
        async logout() {
            if (window.confirm("Are you sure you want to logout?")) {
                console.log("Logging out")
                try {
                    await axios.post("./api/logout/")
                    this.$router.push({ name: "login" })
                } catch (error) {
                    console.log("Logout failed")
                    console.log(error)
                }
            }
        }
    }
})
</script>

<style scoped lang="less">
@import "../vars.less";

ul {
    background-color: darken(@dark_grey, 5%);
    box-shadow: 1px 5px 9px 2px rgba(0, 0, 0, 0.5);
    padding: 0;
    position: absolute;
    top: 100%;
    right: 0;
    width: 15rem;
    margin-top: 0.5rem;

    li {
        text-align: center;
        width: 100%;
        transition: 1s background-color;

        &:hover {
            background-color: rgba(0, 0, 0, 0.2);
            transition: 1s background-color;
        }

        a {
            display: block;
            padding: 0.5rem 1rem;
            box-sizing: border-box;
        }
    }
}
</style>
