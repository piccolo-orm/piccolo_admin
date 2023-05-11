<template>
    <ul>
        <li v-bind:key="key" v-for="(value, key) in customLinks">
            <router-link :to="value" class="subtle">
                <font-awesome-icon icon="level-up-alt" class="rotated90" />
                <span>{{ key | readable }}</span>
            </router-link>
        </li>
    </ul>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        customLinks() {
            return this.$store.state.customLinks
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchCustomLinks")
    }
})
</script>