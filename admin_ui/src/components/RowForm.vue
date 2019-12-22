<template>
    <div>
        <div
            v-bind:key="property.title"
            v-for="property in schema.properties"
        >
            <template v-if="property.foreign_key">
                <label>
                    {{ property.title }}
                    <a
                        class="add"
                        href="#"
                        v-if="!isFilter"
                        v-on:click.prevent="add(property.to)"
                    >
                        <font-awesome-icon icon="plus" />
                    </a>
                </label>
                <KeySelect
                    v-bind:fieldName="property.title.toLowerCase()"
                    v-bind:isFilter="isFilter"
                    v-bind:isNullable="property.nullable"
                    v-bind:tableName="property.to"
                    v-bind:value="getValue(property.title)"
                />
            </template>
            <template v-else>
                <InputField
                    v-bind:format="property.format"
                    v-bind:isFilter="isFilter"
                    v-bind:isNullable="property.nullable"
                    v-bind:key="property.title"
                    v-bind:title="property.title"
                    v-bind:type="property.type || property.anyOf[0].type"
                    v-bind:value="getValue(property.title)"
                />
            </template>
        </div>

        <AddRow
            v-bind:schema="keySchema"
            v-bind:tableName="keyTableName"
            v-if="showAddRow"
            v-on:close="showAddRow = false"
        />
    </div>
</template>

<script>
import KeySelect from "./KeySelect.vue"
import InputField from "./InputField.vue"
import AddRow from "./AddRow.vue"

export default {
    props: {
        row: Object,
        schema: Object,
        isFilter: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            keySchema: undefined,
            keyTableName: undefined,
            showAddRow: false
        }
    },
    components: {
        InputField,
        KeySelect,
        AddRow
    },
    methods: {
        getValue(propertyTitle) {
            let value = this.row
                ? this.row[propertyTitle.toLowerCase().replace(" ", "_")]
                : undefined
            return value
        },
        async add(tableName) {
            let schema = await this.$store.dispatch("fetchSchema", tableName)
            this.keySchema = schema
            this.keyTableName = tableName
            this.showAddRow = true
        }
    }
}
</script>

<style scoped lang="less">
.add {
    float: right;
}
</style>
