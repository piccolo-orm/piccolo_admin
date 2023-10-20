<template>
    <ul>
        <li v-bind:key="title" v-for="(url, title) in customLinks">
            <a :href="url" class="subtle">
                <font-awesome-icon icon="level-up-alt" class="rotated90" />
                <span>{{ title }}</span>
            </a>
        </li>
    </ul>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
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
