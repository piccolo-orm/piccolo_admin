<template>
    <DetailViewBase>
        <ChartsPage :chartSlug="chartSlug" />
    </DetailViewBase>
</template>


<script lang="ts">
import Vue from "vue"
import ChartsPage from "../components/ChartsPage.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default Vue.extend({
    props: ["chartSlug"],
    components: {
        ChartsPage,
        DetailViewBase
    },
    async mounted() {
        await this.$store.dispatch("fetchChartConfig", this.chartSlug)
    }
})
</script>


<style scoped lang="less">
</style>
