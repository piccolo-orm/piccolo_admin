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
                v-bind:columnName="String(columnName)"
                v-bind:type="getType(property)"
                v-bind:value="property.default"
                v-bind:timeResolution="
                    schema?.extra?.time_resolution[columnName]
                "
                v-bind:format="property.format"
            />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"
import InputField from "./InputField.vue"
import { type Schema, getType } from "@/interfaces"

export default defineComponent({
    props: {
        schema: {
            type: Object as PropType<Schema>,
            required: true
        }
    },
    components: {
        InputField
    },
    setup() {
        return {
            getType
        }
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
