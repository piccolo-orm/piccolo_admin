<template>
    <div class="opaque" id="sidebar_overlay" ref="sidebar_overlay">
        <SidebarNav />
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"
import SidebarNav from "./SidebarNav.vue"

const sidebar_overlay = ref<HTMLElement | undefined>(undefined)

onMounted(() => {
    // Make sure the sidebar aligns to the bottom of the nav bar:
    if (sidebar_overlay.value) {
        const navHeight = document
            .querySelector("#nav")
            ?.getBoundingClientRect().height

        if (navHeight) {
            sidebar_overlay.value.style.top = navHeight + "px"
        }
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
    z-index: 1000;

    @media (min-width: @mobile_width) {
        display: none;
    }
}
</style>
