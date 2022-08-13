<template>
    <img :src="'icons/' + logoImage" />
</template>

<script lang="ts">
export default {
    computed: {
        logoImage() {
            return this.$store.state.metaModule.logoImage
        }
    }
}
</script>

<style lang="less" scoped>
img {
    height: 2em;
    width: auto;
    margin: 0.5rem;
}
</style>