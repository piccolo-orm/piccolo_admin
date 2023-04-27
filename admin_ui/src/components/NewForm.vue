<template>
    <div>
        <div
            v-bind:key="property.title"
            v-for="(property, columnName) in schema.properties"
        >
            <label>{{ property.title }}</label>
            <InputField
                v-bind:isFilter="false"
                v-bind:key="columnName"
                v-bind:columnName="columnName"
                v-bind:format="property.format"
                v-bind:title="property.title"
                v-bind:type="property.type || property.anyOf[0].type"
                v-bind:value="property.default"
            />
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"
import InputField from "./InputField.vue"
import { Schema } from "@/interfaces"

export default Vue.extend({
    props: {
        schema: Object as PropType<Schema>
    },
    components: {
        InputField
    }
})
</script>

<style scoped lang="less">
.add {
    float: right;
}

span.required {
    opacity: 0.5;
    padding-left: 0.05rem;
}
</style>
