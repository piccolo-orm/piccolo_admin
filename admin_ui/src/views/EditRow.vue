<template>
    <DetailViewBase>
        <EditRowForm
            :rowID="rowID"
            :tableName="tableName"
        />
    </DetailViewBase>
</template>


<script lang="ts">
import EditRowForm from "../components/EditRowForm.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default {
    props: ["tableName", "rowID"],
    components: {
        EditRowForm,
        DetailViewBase,
    },
}
</script>


<style scoped lang="less"></style>
