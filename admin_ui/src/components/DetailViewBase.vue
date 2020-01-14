<template>
    <div>
        <NavBar />

        <div class="edit_wrapper">
            <p>
                <a
                    href="#"
                    v-on:click.prevent="$router.go(-1)"
                >
                    <font-awesome-icon icon="angle-left" />Back
                </a>
            </p>

            <slot></slot>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import NavBar from "./NavBar.vue"

export default Vue.extend({
    components: {
        NavBar
    }
})
</script>


<style scoped lang="less">
@import "../vars.less";

div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    a {
        text-decoration: none;
    }

    h1 {
        margin: 0;
    }
}
</style>
