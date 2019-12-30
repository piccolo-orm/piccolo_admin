<template>
    <div style="height: 100%;">
        <NavBar />
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
import axios from "axios"
import NavBar from "../components/NavBar.vue"
import SidebarNav from "../components/SidebarNav.vue"

export default Vue.extend({
    components: {
        NavBar,
        SidebarNav
    }
})
</script>


<style lang="less">
@import "../vars.less";

div.wrapper {
    border-top: 1px solid @border_color;
    display: flex;
    height: 100%;

    div.sidebar_wrapper {
        border-right: 1px solid @border_color;
        width: 15rem;

        @media (max-width: @mobile_width) {
            display: none;
        }
    }
}
</style>
