<template>
    <img :src="logoPath" />
</template>

<script lang="ts">
export default {
    computed: {
        logoPath() {
            return this.$store.state.metaModule.logoPath
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