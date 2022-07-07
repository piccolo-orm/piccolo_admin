<template>
    <DropDownMenu>
        <li>
            <a href="#" v-on:click.prevent="logout">
                <font-awesome-icon icon="sign-out-alt" />{{ $t("Log out") }}
            </a>
        </li>
        <li>
            <router-link
                :to="{
                    name: 'changePassword'
                }"
                ><font-awesome-icon icon="key" />{{ $t("Change password") }}
            </router-link>
        </li>
        <li v-if="darkMode">
            <a href="#" v-on:click.prevent="updateDarkMode(false)">
                <font-awesome-icon icon="sun" />{{ $t("Light Mode") }}
            </a>
        </li>
        <li v-else>
            <a href="#" v-on:click.prevent="updateDarkMode(true)">
                <font-awesome-icon icon="moon" />{{ $t("Dark Mode") }}
            </a>
        </li>
        <li>
            <a href="#" v-on:click.prevent="showAboutModal">
                <font-awesome-icon icon="info-circle" />{{ $t("About") }}
                Piccolo
            </a>
        </li>
    </DropDownMenu>
</template>

<script lang="ts">
import axios from "axios"
import Vue from "vue"

import DropDownMenu from "./DropDownMenu.vue"

export default Vue.extend({
    components: {
        DropDownMenu
    },
    computed: {
        darkMode() {
            return this.$store.state.darkMode
        }
    },
    methods: {
        updateDarkMode(enabled: boolean) {
            this.$store.commit("updateDarkMode", enabled)
        },
        showAboutModal() {
            this.$store.commit("updateShowAboutModal", true)
        },
        async logout() {
            if (window.confirm("Are you sure you want to logout?")) {
                console.log("Logging out")
                try {
                    await axios.post("./auth/logout/")
                    // Reload the entire page, rather than using vue-router,
                    // otherwise some data from Vuex will remain in memory.
                    // The app will redirect the user to the login page
                    // after the reload.
                    location.replace(window.location.pathname)
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
</style>
