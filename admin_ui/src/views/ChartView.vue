<template>
    <DetailViewBase>
        <Chart :chartSlug="chartSlug" />
    </DetailViewBase>
</template>

<script lang="ts">
import Vue from "vue"
import Chart from "../components/Chart.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default Vue.extend({
    props: {
        chartSlug: String
    },
    components: {
        Chart,
        DetailViewBase
    }
})
</script>

<style scoped lang="less"></style>
