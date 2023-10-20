<template>
    <div class="opaque" id="sidebar_overlay">
        <SidebarNav />
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import SidebarNav from "./SidebarNav.vue"

export default defineComponent({
    components: {
        SidebarNav
    }
})
</script>

<style lang="less">
@import "../vars.less";

div#sidebar_overlay {
    position: absolute;
    top: 3.6rem;
    left: 0;
    max-width: 15rem;
    min-width: 10rem;
    bottom: 0;
    border-right: 1px solid @border_color;
    border-top: 1px solid @border_color;
    z-index: 1000;

    @media (min-width: @mobile_width) {
        display: none;
    }
}
</style>
