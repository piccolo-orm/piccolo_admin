<template>
    <div>
        <div
            v-bind:key="property.title"
            v-for="(property, keyName) in schema.properties"
        >
            <template v-if="property.extra.foreign_key">
                <label>
                    {{ property.title }}
                    <span
                        class="required"
                        v-if="isRequired(keyName)"
                    >*</span>

                    <router-link
                        :to="{name: 'addRow', params: {tableName: property.extra.to}}"
                        class="add"
                        target="_blank"
                        v-if="!isFilter"
                    >
                        <font-awesome-icon icon="plus" />
                    </router-link>

                    <router-link
                        :to="{name: 'editRow', params: {tableName: property.extra.to, rowID: getKeySelectID(property.title)}}"
                        class="add"
                        target="_blank"
                        v-if="!isFilter"
                    >
                        <font-awesome-icon icon="edit" />
                    </router-link>
                </label>
                <KeySearch
                    v-bind:fieldName="property.title.toLowerCase()"
                    v-bind:key="getValue(property.title)"
                    v-bind:tableName="property.extra.to"
                    v-bind:value="getValue(property.title)"
                />
            </template>
            <template v-else>
                <label>
                    {{ property.title }}
                    <span
                        class="required"
                        v-if="isRequired(keyName)"
                    >*</span>
                </label>
                <InputField
                    v-bind:format="property.format"
                    v-bind:isFilter="isFilter"
                    v-bind:isNullable="property.nullable"
                    v-bind:key="property.title"
                    v-bind:required="isRequired(keyName)"
                    v-bind:title="property.title"
                    v-bind:type="property.type || property.anyOf[0].type"
                    v-bind:value="getValue(property.title)"
                />
            </template>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue"

import KeySearch from "./KeySearch.vue"
import InputField from "./InputField.vue"

export default Vue.extend({
    props: {
        row: Object,
        schema: Object,
        isFilter: {
            type: Boolean,
            default: false,
        },
    },
    components: {
        InputField,
        KeySearch,
    },
    data() {
        return {
            keySelectIDs: {},
        }
    },
    methods: {
        getValue(propertyTitle: string) {
            let value = this.row
                ? this.row[propertyTitle.toLowerCase().split(" ").join("_")]
                : undefined
            return value
        },
        getKeySelectID(propertyTitle: string) {
            return this.getValue(propertyTitle)
        },
        isRequired(keyName: string) {
            return (
                !this.isFilter &&
                (this.schema.required || []).indexOf(keyName) != -1
            )
        },
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