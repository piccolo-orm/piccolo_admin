<template>
    <div>
        <template v-if="type == 'integer'">
            <OperatorField
                :fieldName="getFieldName(title)"
                v-if="isFilter"
            />
            <input
                step="1"
                type="number"
                v-bind:name="getFieldName(title)"
                v-bind:placeholder="placeholder"
                v-bind:value="value"
            />
        </template>

        <template v-if="type == 'string'">
            <template v-if="format == 'date-time'">
                <OperatorField
                    :fieldName="title.toLowerCase()"
                    v-if="isFilter"
                />
                <flat-pickr
                    v-bind:config="{ enableTime: true }"
                    v-bind:name="getFieldName(title)"
                    v-model="localValue"
                ></flat-pickr>
            </template>

            <div v-else-if="format == 'text-area' && isFilter == false">
                <textarea
                    autocomplete="off"
                    ref="textarea"
                    v-bind:name="getFieldName(title)"
                    v-bind:placeholder="placeholder"
                    v-bind:style="{height: textareaHeight}"
                    v-model="localValue"
                    v-on:input="setTextareaHeight"
                />
            </div>

            <input
                type="text"
                v-bind:name="getFieldName(title)"
                v-bind:placeholder="placeholder"
                v-else
                v-model="localValue"
            />
        </template>

        <template v-if="type == 'boolean'">
            <select v-bind:name="getFieldName(title)">
                <option
                    v-bind:selected="value == 'all'"
                    v-if="isFilter"
                    value="all"
                >All</option>
                <option
                    v-bind:selected="value == null"
                    v-if="isNullable"
                    value="null"
                >Null</option>
                <option
                    v-bind:selected="value == true"
                    value="true"
                >True</option>
                <option
                    v-bind:selected="value == false"
                    value="false"
                >False</option>
            </select>
        </template>

        <template v-if="type == 'number'">
            <OperatorField
                :fieldName="title.toLowerCase()"
                v-if="isFilter"
            />
            <input
                type="text"
                v-bind:name="getFieldName(title)"
                v-bind:placeholder="placeholder"
                v-model="localValue"
            />
        </template>
    </div>
</template>

<script lang="ts">
import Vue from "vue"

import flatPickr from "vue-flatpickr-component"
import OperatorField from "./OperatorField.vue"

export default {
    props: {
        title: String,
        type: String,
        value: undefined,
        format: String,
        isFilter: {
            type: Boolean,
            default: true
        },
        isNullable: {
            type: Boolean,
            default: false
        }
    },
    components: {
        flatPickr,
        OperatorField
    },
    data() {
        return {
            localValue: undefined,
            textareaHeight: "50px"
        }
    },
    computed: {
        placeholder() {
            return this.isFilter ? "All" : ""
        }
    },
    methods: {
        getFieldName(name: string) {
            return name
                .toLowerCase()
                .split(" ")
                .join("_")
        },
        setTextareaHeight() {
            let element = this.$refs.textarea
            if (element) {
                if (element.scrollHeight > element.clientHeight) {
                    this.textareaHeight = element.scrollHeight + "px"
                }
            }
        }
    },
    watch: {
        value() {
            this.localValue = this.value
            this.setTextareaHeight()
        }
    },
    mounted() {
        this.localValue = this.value

        let app = this
        setTimeout(function() {
            app.setTextareaHeight()
        }, 0)
    }
}
</script>
