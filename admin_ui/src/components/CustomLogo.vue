<template>
    <img
        :src="'icons/' + logoImage"
        :width="logoWidth"
        :height="logoHeight"
        id="logo"
    />
</template>

<script lang="ts">
export default {
    computed: {
        logoImage() {
            return this.$store.state.metaModule.logoImage
        },
        logoWidth() {
            return this.$store.state.metaModule.logoWidth
        },
        logoHeight() {
            return this.$store.state.metaModule.logoHeight
        }
    }
}
</script>

<style lang="less" scoped>
#logo {
    margin: 1rem;
}
</style>