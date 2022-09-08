<template>
    <div v-if="row">
        <div
            v-bind:key="columnName"
            v-for="(property, columnName) in schema.properties"
        >
            <template v-if="property.extra.foreign_key">
                <label>
                    {{ property.title }}
                    <span class="required" v-if="isRequired(String(columnName))">*</span>
                    <Tooltip
                        v-if="property.extra.help_text"
                        :content="property.extra.help_text"
                    />

                    <router-link
                        :to="{
                            name: 'addRow',
                            params: { tableName: property.extra.to }
                        }"
                        class="add"
                        target="_blank"
                        v-if="!isFilter"
                    >
                        <font-awesome-icon icon="plus" />
                    </router-link>

                    <router-link
                        :to="{
                            name: 'editRow',
                            params: {
                                tableName: property.extra.to,
                                rowID: getKeySelectID(property.title)
                            }
                        }"
                        class="add"
                        target="_blank"
                        v-if="!isFilter"
                    >
                        <font-awesome-icon icon="edit" />
                    </router-link>
                </label>
                <KeySearch
                    v-bind:fieldName="columnName"
                    v-bind:tableName="property.extra.to"
                    v-bind:rowID="getValue(String(columnName))"
                    v-bind:readable="getValue(columnName + '_readable')"
                    v-bind:isNullable="property.nullable"
                />
            </template>
            <template v-else>
                <label>
                    {{ property.title }}
                    <span class="required" v-if="isRequired(String(columnName))">*</span>
                    <Tooltip
                        v-if="property.extra.help_text"
                        :content="property.extra.help_text"
                    />
                </label>
                <InputField
                    v-bind:columnName="columnName"
                    v-bind:format="property.format"
                    v-bind:isFilter="isFilter"
                    v-bind:isNullable="property.nullable"
                    v-bind:required="isRequired(String(columnName))"
                    v-bind:title="property.title"
                    v-bind:type="property.type || property.anyOf[0].type"
                    v-bind:value="getValue(String(columnName))"
                    v-bind:choices="property.extra.choices"
                    v-bind:isMediaColumn="isMediaColumn(String(columnName))"
                    v-bind:isRichText="isRichText(String(columnName))"
                />
            </template>
        </div>
    </div>
</template>

<script lang="ts">
import Vue, {PropType} from "vue"

import KeySearch from "./KeySearch.vue"
import InputField from "./InputField.vue"
import Tooltip from "./Tooltip.vue"
import {Schema} from "@/interfaces"

export default Vue.extend({
    props: {
        row: Object,
        schema: Object as PropType<Schema>,
        isFilter: {
            type: Boolean,
            default: false
        }
    },
    components: {
        InputField,
        KeySearch,
        Tooltip
    },
    data() {
        return {
            keySelectIDs: {},
            baseIndex: 1,
            windowListener: undefined
        }
    },
    methods: {
        getValue(columnName: string) {
            let value = this.row
                ? this.row[columnName]
                : undefined
            return value
        },
        getKeySelectID(propertyTitle: string) {
            return (
                this.keySelectIDs[propertyTitle] || this.getValue(propertyTitle)
            )
        },
        keySelectChanged(propertyTitle: string, value: number) {
            console.log(`${propertyTitle} = ${value}`)
            Vue.set(this.keySelectIDs, propertyTitle, value)
        },
        // We use this to refresh KeySelect components
        getKey(keyName: string) {
            return keyName + this.baseIndex
        },
        isRequired(keyName: string) {
            return (
                !this.isFilter &&
                (this.schema.required || []).indexOf(keyName) != -1
            )
        },
        isMediaColumn(keyName: string) {
            return this.schema.media_columns.includes(keyName)
        },
        isRichText(keyName: string) {
            return this.schema.rich_text_columns.includes(keyName)
        }
    },
    mounted() {
        window.addEventListener("message", receiveMessage, false)

        let app = this

        function receiveMessage(event) {
            if (event.origin !== document.location.origin) return
            console.log("Received message")
            app.baseIndex = app.baseIndex + 1
        }

        this.windowListener = receiveMessage
    },
    destroyed() {
        if (this.windowListener) {
            window.removeEventListener("message", this.windowListener)
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
