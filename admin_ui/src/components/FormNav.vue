<template>
    <ul>
        <li v-bind:key="formConfig.name" v-for="formConfig in formConfigs">
            <router-link
                :to="{ name: 'addForm', params: { formSlug: formConfig.slug } }"
                class="subtle"
            >
                <font-awesome-icon icon="level-up-alt" class="rotated90" />
                <span>{{ formConfig.name | readable }}</span>
            </router-link>
        </li>
    </ul>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        formConfigs() {
            return this.$store.state.formConfigs
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchFormConfigs")
    }
})
</script>
