<template>
    <DetailViewBase>
        <EditRowForm
            :rowID="rowID"
            :tableName="tableName"
        />
    </DetailViewBase>
</template>


<script lang="ts">
import { defineComponent } from "vue"
import EditRowForm from "../components/EditRowForm.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default defineComponent({
    props: ["tableName", "rowID"],
    components: {
        EditRowForm,
        DetailViewBase,
    },
})
</script>


<style scoped lang="less"></style>
