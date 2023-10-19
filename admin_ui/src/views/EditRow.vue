<template>
    <DetailViewBase>
        <EditRowForm :rowID="rowID" :tableName="tableName" />
    </DetailViewBase>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import type { RowID } from "@/interfaces"
import EditRowForm from "../components/EditRowForm.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>,
            required: true
        },
        rowID: {
            type: undefined as unknown as PropType<RowID>,
            required: true
        }
    },
    components: {
        EditRowForm,
        DetailViewBase
    }
})
</script>

<style scoped lang="less"></style>
