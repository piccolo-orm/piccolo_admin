<template>
    <div class="base_view">
        <NavBar :username="username" :siteName="siteName" />
        <div class="wrapper">
            <div class="sidebar_wrapper">
                <SidebarNav />
            </div>
            <slot></slot>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import NavBar from "../components/NavBar.vue"
import SidebarNav from "../components/SidebarNav.vue"

export default Vue.extend({
    components: {
        NavBar,
        SidebarNav
    },
    computed: {
        username() {
            const user = this.$store.state.user
            return user ? user.username : "Unknown"
        },
        siteName() {
            return this.$store.state.metaModule.siteName
        }
    }
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
