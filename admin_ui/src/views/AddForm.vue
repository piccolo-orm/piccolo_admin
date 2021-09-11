<template>
    <DetailViewBase>
        <FormAdd
            :formName="formName"
            :schema="schema"
            v-if="schema"
        />
    </DetailViewBase>
</template>


<script lang="ts">
import Vue from "vue"
import FormAdd from "../components/FormAdd.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default Vue.extend({
    props: ["formName"],
    components: {
        FormAdd,
        DetailViewBase,
    },
    computed: {
        schema() {
            return this.$store.state.formSchema
        },
    },
    async mounted() {
        this.$store.commit("updateCurrentFormname", this.formName)
        await this.$store.dispatch("fetchFormSchema", this.formName)
    },
})
</script>


<style scoped lang="less">
</style>
