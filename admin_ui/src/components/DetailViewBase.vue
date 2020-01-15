<template>
    <div>
        <NavBar />

        <div class="inner">
            <BackButton />

            <slot></slot>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import BackButton from "./BackButton.vue"
import NavBar from "./NavBar.vue"

export default Vue.extend({
    components: {
        BackButton,
        NavBar
    }
})
</script>


<style scoped lang="less">
@import "../vars.less";

div.inner {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    h1 {
        margin: 0;
    }

    a {
        text-decoration: none;
    }
}
</style>
