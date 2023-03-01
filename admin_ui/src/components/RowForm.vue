<template>
    <div v-if="row">
        <div
            v-bind:key="columnName"
            v-for="(property, columnName) in schema.properties"
        >
            <label
                v-bind:style="
                    isReadOnly(String(columnName)) ? 'display:none' : ''
                "
            >
                {{ property.title }}
                <span class="required" v-if="isRequired(String(columnName))"
                    >*</span
                >
                <Tooltip
                    v-if="property.extra.help_text"
                    :content="property.extra.help_text"
                />

                <template
                    v-if="property.extra.foreign_key"
                    v-bind:style="
                        isReadOnly(String(columnName)) ? 'display:none' : ''
                    "
                >
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
                        v-if="!isFilter && foreignKeyIDs[columnName]"
                        :to="{
                            name: 'editRow',
                            params: {
                                tableName: property.extra.to,
                                rowID: foreignKeyIDs[columnName]
                            }
                        }"
                        class="add"
                        target="_blank"
                    >
                        <font-awesome-icon icon="edit" />
                    </router-link>
                </template>
            </label>

            <KeySearch
                v-if="property.extra.foreign_key"
                v-bind:fieldName="String(columnName)"
                v-bind:tableName="property.extra.to"
                v-bind:rowID="getValue(String(columnName))"
                v-bind:readable="getValue(columnName + '_readable')"
                v-bind:isNullable="property.nullable"
                v-bind:style="
                    isReadOnly(String(columnName)) ? 'display:none' : ''
                "
                @update="$set(foreignKeyIDs, String(columnName), $event.id)"
            />
            <InputField
                v-else
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
                v-bind:style="
                    isReadOnly(String(columnName)) ? 'display:none' : ''
                "
            />
        </div>
    </div>
</template>

<script lang="ts">
import Vue, { computed, PropType, reactive, toRefs, watch } from "vue"

import KeySearch from "./KeySearch.vue"
import InputField from "./InputField.vue"
import Tooltip from "./Tooltip.vue"
import { Schema } from "@/interfaces"

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
    setup(props) {
        const { schema, row } = toRefs(props)

        const foreignKeyColumnNames = computed(() => {
            const _foreignKeyColumnNames = []

            Object.entries(schema.value.properties).forEach((value) => {
                const [columnName, property] = value
                if (property.extra.foreign_key == true) {
                    _foreignKeyColumnNames.push(columnName)
                }
            })

            return _foreignKeyColumnNames
        })

        const foreignKeyIDs = computed(() => {
            const _foreignKeyIDs = {}
            foreignKeyColumnNames.value.forEach((columnName) => {
                _foreignKeyIDs[columnName] = row.value[columnName]
            })

            return reactive(_foreignKeyIDs)
        })

        return {
            foreignKeyIDs
        }
    },
    methods: {
        getValue(columnName: string) {
            let value = this.row ? this.row[columnName] : undefined
            return value
        },
        isRequired(columnName: string) {
            return (
                !this.isFilter &&
                (this.schema.required || []).indexOf(columnName) != -1
            )
        },
        isMediaColumn(columnName: string) {
            return this.schema.media_columns.includes(columnName)
        },
        isRichText(columnName: string) {
            return this.schema.rich_text_columns.includes(columnName)
        },
        isReadOnly(columnName: string) {
            return (
                this.schema.read_only_columns.includes(columnName) &&
                this.$route.params.rowID
            )
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
