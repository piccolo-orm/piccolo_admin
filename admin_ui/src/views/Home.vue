<template>
    <BaseView>
        <div class="welcome">
            <h1>Welcome to {{ siteName }}</h1>
            <p>Select one of the tables in the sidebar to get started.</p>
        </div>
    </BaseView>
</template>

<script lang="ts">
import BaseView from "./BaseView.vue"

export default {
    components: {
        BaseView,
    },
    computed: {
        siteName() {
            return this.$store.state.metaModule.siteName
        },
    },
    mounted() {
        this.$store.commit("updateCurrentTablename", "")
    },
    async created() {
        await this.$store.dispatch("fetchMeta")
    },
}
</script>

<style scoped lang="less">
div.welcome {
    padding: 0 1rem;
}
</style>