<template>
    <BaseView>
        <div class="welcome">
            <h1>{{ $t("Welcome to") }} {{ siteName }}</h1>
            <p>
                {{
                    $t(
                        "Select one of the tables in the sidebar to get started."
                    )
                }}
            </p>
        </div>
    </BaseView>
</template>

<script lang="ts">
import BaseView from "./BaseView.vue"

export default {
    components: {
        BaseView
    },
    computed: {
        siteName() {
            return this.$store.state.metaModule.siteName
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchLanguages")
        this.$store.commit("updateCurrentTablename", "")
    }
}
</script>

<style scoped lang="less">
div.welcome {
    padding: 0 1rem;
}
</style>