<template>
    <div>
        <NavBar />
        <div class="wrapper">
            <SidebarNav />
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
}
</style>
