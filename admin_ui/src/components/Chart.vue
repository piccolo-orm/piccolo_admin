<template>
    <div v-if="chartConfig">
        <h3>{{ chartConfig.title }}</h3>
        <pie-chart
            width="650px"
            height="450px"
            :download="{ background: '#ffffff' }"
            v-if="chartConfig.chart_type == 'Pie'"
            :data="chartData"
        ></pie-chart>
        <line-chart
            width="650px"
            height="450px"
            :download="{ background: '#ffffff' }"
            v-else-if="chartConfig.chart_type == 'Line'"
            :data="chartData"
        ></line-chart>
        <column-chart
            width="650px"
            height="450px"
            :download="{ background: '#ffffff' }"
            v-else-if="chartConfig.chart_type == 'Column'"
            :data="chartData"
        ></column-chart>
        <bar-chart
            width="650px"
            height="450px"
            :download="{ background: '#ffffff' }"
            v-else-if="chartConfig.chart_type == 'Bar'"
            :data="chartData"
        ></bar-chart>
        <area-chart
            width="650px"
            height="450px"
            :download="{ background: '#ffffff' }"
            v-else-if="chartConfig.chart_type == 'Area'"
            :data="chartData"
        ></area-chart>
    </div>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    data() {
        return { chartData: [], chartConfig: null, chartSchema: null }
    },
    async mounted() {
        const chartSlug = this.$router.currentRoute.params.chartSlug

        this.chartData = (
            await this.$store.dispatch("fetchChartData", chartSlug)
        ).data

        this.chartConfig = (
            await this.$store.dispatch("fetchChartConfig", chartSlug)
        ).data

        if (this.chartConfig.has_form) {
            this.chartSchema = (
                await this.$store.dispatch("fetchChartSchema", chartSlug)
            ).data
        }
    }
})
</script>

<style scoped lang="less">
h3 {
    text-transform: capitalize;
    text-align: center;
}
</style>
