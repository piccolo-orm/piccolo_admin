<template>
    <div class="base_view">
        <NavBar
            :siteName="siteName"
            :username="username"
        />
        <div class="wrapper">
            <div class="sidebar_wrapper">
                <SidebarNav />
            </div>
            <slot></slot>
        </div>
    </div>
</template>


<script lang="ts">
import { defineComponent } from "vue"
import NavBar from "../components/NavBar.vue"
import SidebarNav from "../components/SidebarNav.vue"

export default defineComponent({
    components: {
        NavBar,
        SidebarNav,
    },
    computed: {
        username() {
            const user: any = this.$store.state.user
            return user ? user.username : "Unknown"
        },
        siteName() {
            return this.$store.state.siteName
        },
    },
})
</script>


<style lang="less">
@import "../vars.less";

div.base_view {
    flex-grow: 1;
    display: flex;
    flex-direction: column;

    div.wrapper {
        border-top: 1px solid @border_color;
        display: flex;
        flex-grow: 1;

        div.sidebar_wrapper {
            border-right: 1px solid @border_color;
            width: 15rem;

            @media (max-width: @mobile_width) {
                display: none;
            }
        }
    }
}
</style>
