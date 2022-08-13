<template>
    <img
        :src="'icons/' + logoName"
        :width="logoWidth"
        :height="logoHeight"
        id="logo"
    />
</template>

<script lang="ts">
export default {
    computed: {
        logoName() {
            return this.$store.state.metaModule.logoName
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