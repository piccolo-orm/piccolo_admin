<template>
    <ul>
        <li v-bind:key="formConfig.name" v-for="formConfig in formConfigs">
            <router-link
                :to="{ name: 'addForm', params: { formSlug: formConfig.slug } }"
                class="subtle"
            >
                <font-awesome-icon icon="level-up-alt" class="rotated90" />
                <span>{{ readable(formConfig.name) }}</span>
            </router-link>
        </li>
    </ul>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import { readable } from "@/utils"

export default defineComponent({
    computed: {
        formConfigs() {
            return this.$store.state.formConfigs
        }
    },
    setup() {
        return {
            readable
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchFormConfigs")
    }
})
</script>
