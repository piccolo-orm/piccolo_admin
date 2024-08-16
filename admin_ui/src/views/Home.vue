<template>
    <BaseView>
        <div class="welcome">
            <h1>{{ $t("Welcome to") }} {{ siteName }}</h1>
            <p>
                {{ $t("Select a table in the sidebar to get started.") }}
            </p>
            <p>
                <a href="/api/mfa-setup/">
                    <font-awesome-icon icon="mobile-alt" />{{ $t("MFA Setup") }}
                </a>
            </p>
        </div>
    </BaseView>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import BaseView from "./BaseView.vue"

export default defineComponent({
    components: {
        BaseView
    },
    computed: {
        siteName() {
            return this.$store.state.metaModule.siteName
        }
    },
    mounted() {
        this.$store.commit("updateCurrentTablename", "")
    }
})
</script>

<style scoped lang="less">
div.welcome {
    padding: 0 1rem;
}
</style>
