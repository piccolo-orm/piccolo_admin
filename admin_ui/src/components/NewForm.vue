<template>
    <div>
        <div
            v-bind:key="property.title"
            v-for="(property, keyName) in schema.properties"
        >
            <label>{{ property.title }}</label>
            <InputField
                v-bind:isFilter="isFilter"
                v-bind:key="keyName"
                v-bind:title="property.title"
                v-bind:type="property.type || property.anyOf[0].type"
            />
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue"
import InputField from "./InputField.vue"

export default Vue.extend({
    props: {
        schema: Object,
        isFilter: {
            type: Boolean,
            default: false,
        },
    },
    components: {
        InputField,
    },
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
