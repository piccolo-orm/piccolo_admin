<template>
    <div>
        <h3>{{ chartConfigs.title }}</h3>
        <pie-chart
            v-if="chartConfigs.chart_type == 'Pie'"
            :data="chartConfigs.data"
        ></pie-chart>
        <line-chart
            v-else-if="chartConfigs.chart_type == 'Line'"
            :data="chartConfigs.data"
        ></line-chart>
        <column-chart
            v-else-if="chartConfigs.chart_type == 'Column'"
            :data="chartConfigs.data"
        ></column-chart>
        <bar-chart
            v-else-if="chartConfigs.chart_type == 'Bar'"
            :data="chartConfigs.data"
        ></bar-chart>
        <area-chart
            v-else-if="chartConfigs.chart_type == 'Area'"
            :data="chartConfigs.data"
        ></area-chart>
    </div>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        chartConfigs() {
            return this.$store.state.chartConfigs
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
