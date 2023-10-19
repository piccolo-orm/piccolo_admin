<template>
    <div>
        <NavBar :username="username" :siteName="siteName" />

        <div class="inner">
            <BackButton />

            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import BackButton from "./BackButton.vue"
import NavBar from "./NavBar.vue"

export default defineComponent({
    components: {
        BackButton,
        NavBar
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

<style scoped lang="less">
@import "../vars.less";

div.inner {
    margin: 0 auto;
    max-width: 40rem;
    padding: 1rem 0.5rem;

    h1 {
        margin: 0;
    }

    a {
        text-decoration: none;
    }
}
</style>
