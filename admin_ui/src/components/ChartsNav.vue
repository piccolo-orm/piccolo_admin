<template>
    <ul>
        <li v-bind:key="chartConfig.title" v-for="chartConfig in chartConfigs">
            <router-link
                :to="{
                    name: 'getCharts',
                    params: { chartSlug: chartConfig.chart_slug }
                }"
                class="subtle"
            >
                <font-awesome-icon icon="level-up-alt" class="rotated90" />
                <span>{{ chartConfig.title }}</span>
            </router-link>
        </li>
    </ul>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        chartConfigs() {
            return this.$store.state.chartConfigs
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchChartConfigs")
    }
})
</script>