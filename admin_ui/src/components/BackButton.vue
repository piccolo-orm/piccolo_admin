<template>
    <p>
        <a
            href="#"
            v-if="showBackButton"
            v-on:click.prevent="$router.go(-1)"
        >
            <font-awesome-icon icon="angle-left" />Back
        </a>
    </p>
</template>

<script>
export default {
    computed: {
        showBackButton() {
            return window.history.length > 1
        }
    }
}
</script>

<style lang="less">
a {
    text-decoration: none;
}
</style>
