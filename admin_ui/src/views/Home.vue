<template>
    <BaseView>
        <div class="welcome">
            <h1>Welcome to {{ siteName }}</h1>
            <p>Select one of the tables in the sidebar to get started.</p>
        </div>
    </BaseView>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import BaseView from "./BaseView.vue"

export default defineComponent({
    components: {
        BaseView,
    },
    computed: {
        siteName() {
            return this.$store.state.siteName
        },
    },
    mounted() {
        this.$store.commit("updateCurrentTablename", "")
    },
})
</script>

<style scoped lang="less">
div.welcome {
    padding: 0 1rem;
}
</style>