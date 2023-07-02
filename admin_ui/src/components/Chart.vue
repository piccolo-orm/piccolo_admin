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

        <form @submit.prevent="handleSubmit($event)" v-if="chartSchema">
            <NewForm :schema="chartSchema"></NewForm>
            <button>Apply</button>
        </form>
    </div>
</template>

<script lang="ts">
import Vue from "vue"
import NewForm from "./NewForm.vue"
import { convertFormValue } from "@/utils"

export default Vue.extend({
    data() {
        return {
            chartData: [],
            chartConfig: null,
            chartSchema: null,
            chartSlug: null
        }
    },
    components: { NewForm },
    methods: {
        async handleSubmit(event) {
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                const key = i[0]
                let value = i[1]

                json[key] = convertFormValue({
                    key,
                    value,
                    schema: this.chartSchema
                })
            }

            this.chartData = (
                await this.$store.dispatch("fetchChartData", {
                    chartSlug: this.chartSlug,
                    data: json
                })
            ).data
        }
    },
    async mounted() {
        this.chartSlug = this.$router.currentRoute.params.chartSlug

        this.chartData = (
            await this.$store.dispatch("fetchChartData", {
                chartSlug: this.chartSlug,
                data: {}
            })
        ).data

        this.chartConfig = (
            await this.$store.dispatch("fetchChartConfig", this.chartSlug)
        ).data

        if (this.chartConfig.has_form) {
            this.chartSchema = (
                await this.$store.dispatch("fetchChartSchema", this.chartSlug)
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
