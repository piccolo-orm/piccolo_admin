<template>
    <DropDownMenu>
        <li>
            <a href="#" v-on:click.prevent="logout" data-uitest="logout_button">
                <font-awesome-icon icon="sign-out-alt" />{{ $t("Log Out") }}
            </a>
        </li>
        <li>
            <router-link
                :to="{
                    name: 'changePassword'
                }"
                ><font-awesome-icon icon="key" />{{ $t("Change Password") }}
            </router-link>
        </li>
        <li>
            <a href="./api/mfa-setup/" @click="$event.stopPropagation()">
                <font-awesome-icon icon="mobile-alt" />{{ $t("MFA Setup") }}
            </a>
        </li>
        <li v-if="darkMode">
            <a href="#" @click.prevent="updateDarkMode(false)">
                <font-awesome-icon icon="sun" />{{ $t("Light Mode") }}
            </a>
        </li>
        <li v-else>
            <a href="#" @click.prevent="updateDarkMode(true)">
                <font-awesome-icon icon="moon" />{{ $t("Dark Mode") }}
            </a>
        </li>
        <li>
            <a href="#" @click.prevent="showTimezoneModal"
                ><font-awesome-icon icon="globe" />{{ $t("Set Timezone") }}</a
            >
        </li>
        <li>
            <a href="#" @click.prevent="showAboutModal">
                <font-awesome-icon icon="info-circle" />{{ $t("About") }}
                Piccolo
            </a>
        </li>
    </DropDownMenu>
</template>

<script lang="ts">
import axios from "axios"
import { defineComponent } from "vue"

import DropDownMenu from "./DropDownMenu.vue"

export default defineComponent({
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
        showTimezoneModal() {
            this.$store.commit("updateShowTimezoneModal", true)
        },
        async logout() {
            if (window.confirm("Are you sure you want to logout?")) {
                console.log("Logging out")
                try {
                    await axios.post("./public/logout/")
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

<style scoped lang="less"></style>
