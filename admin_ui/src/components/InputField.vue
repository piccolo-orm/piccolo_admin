<template>
    <div>
        <template v-if="choices">
            <OperatorField :fieldName="getFieldName(title)" v-if="isFilter" />
            <ChoiceSelect
                :choices="choices"
                :fieldName="getFieldName(title)"
                :isFilter="isFilter"
                :isNullable="isNullable"
                :value="value"
            />
        </template>

        <template v-else-if="type == 'integer'">
            <OperatorField :fieldName="getFieldName(title)" v-if="isFilter" />
            <input
                step="1"
                type="number"
                v-bind:name="getFieldName(title)"
                v-bind:placeholder="placeholder"
                v-bind:value="value"
            />
        </template>

        <template v-else-if="type == 'string'">
            <template v-if="format == 'date-time'">
                <OperatorField
                    :fieldName="getFieldName(title)"
                    v-if="isFilter"
                />
                <!--
                `disableMobile` is very poorly named - setting it to 'true'
                enables the picker on mobile devices. It doesn't work great on
                iOS, so an alternative picker is needed.
                -->
                <flat-pickr
                    v-bind:config="{ enableTime: true, disableMobile: 'true' }"
                    v-bind:name="getFieldName(title)"
                    v-model="localValue"
                ></flat-pickr>
            </template>

            <div v-else-if="format == 'text-area' && isFilter == false">
                <textarea
                    v-if="
                        !schema.rich_text_columns.includes(
                            getFieldName(title).toLowerCase()
                        )
                    "
                    autocomplete="off"
                    ref="textarea"
                    v-bind:name="getFieldName(title)"
                    v-bind:placeholder="placeholder"
                    v-bind:style="{ height: textareaHeight }"
                    v-model="localValue"
                    v-on:input="setTextareaHeight"
                />
                <vue-editor
                    v-else
                    v-model="localValue"
                    v-bind:name="getFieldName(title)"
                    :editor-toolbar="customToolbar"
                />

                <textarea
                    id="editor"
                    v-model.lazy="localValue"
                    v-bind:name="getFieldName(title)"
                ></textarea>
            </div>

            <div v-else-if="format == 'json'">
                <textarea
                    :value="JSON.stringify(JSON.parse(value), null, 2)"
                    autocomplete="off"
                    ref="textarea"
                    v-bind:name="getFieldName(title)"
                    v-bind:style="{ height: textareaHeight }"
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

        <template v-else-if="type == 'boolean'">
            <select v-bind:name="getFieldName(title)">
                <option
                    v-bind:selected="value == 'all'"
                    v-if="isFilter"
                    value="all"
                >
                    All
                </option>
                <option
                    v-bind:selected="value == null"
                    v-if="isNullable"
                    value="null"
                >
                    Null
                </option>
                <option v-bind:selected="value == true" value="true">
                    True
                </option>
                <option v-bind:selected="value == false" value="false">
                    False
                </option>
            </select>
        </template>

        <template v-else-if="type == 'number'">
            <template v-if="format == 'time-delta'">
                <OperatorField
                    :fieldName="title.toLowerCase()"
                    v-if="isFilter"
                />
                <DurationWidget
                    v-bind:timedelta="localValue"
                    v-on:newTimedelta="updateLocalValue($event)"
                />
                <input
                    type="hidden"
                    v-bind:name="getFieldName(title)"
                    v-model="localValue"
                />
            </template>
            <template v-else>
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
        </template>

        <template v-else-if="type == 'array'">
            <ArrayWidget
                :array="localValue"
                v-on:updateArray="localValue = $event"
            />
            <input
                :value="JSON.stringify(localValue)"
                type="hidden"
                v-bind:name="getFieldName(title)"
            />
        </template>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"

import flatPickr from "vue-flatpickr-component"

import ArrayWidget from "./ArrayWidget.vue"
import ChoiceSelect from "./ChoiceSelect.vue"
import DurationWidget from "./DurationWidget.vue"
import OperatorField from "./OperatorField.vue"
import { Choices } from "../interfaces"
import { VueEditor } from "vue2-editor"

export default Vue.extend({
    props: {
        title: {
            type: String,
            default: ""
        },
        type: {
            type: String,
            default: "string"
        },
        value: {
            type: undefined,
            default: undefined
        },
        // Fields can share the same type, but have different formats. For
        // example, 'text-area', when type is 'string'.
        format: String,
        isFilter: {
            type: Boolean,
            default: true
        },
        isNullable: {
            type: Boolean,
            default: false
        },
        choices: {
            type: Object as PropType<Choices>,
            default: null
        }
    },
    components: {
        flatPickr,
        ArrayWidget,
        ChoiceSelect,
        DurationWidget,
        OperatorField,
        VueEditor
    },
    data() {
        return {
            localValue: undefined,
            textareaHeight: "50px",
            customToolbar: [
                ["bold", "italic", "underline", "strike", "blockquote"],
                [{ list: "ordered" }, { list: "bullet" }],
                [{ indent: "-1" }, { indent: "+1" }],
                [
                    { align: "" },
                    { align: "center" },
                    { align: "right" },
                    { align: "justify" }
                ],
                ["link", "image", "code-block"]
            ]
        }
    },
    computed: {
        placeholder() {
            return this.isFilter ? "All" : ""
        },
        schema() {
            return this.$store.state.schema
        }
    },
    methods: {
        getFieldName(name: string) {
            return name.toLowerCase().split(" ").join("_")
        },
        setTextareaHeight() {
            let element = this.$refs.textarea
            if (element) {
                if (element.scrollHeight > element.clientHeight) {
                    this.textareaHeight = element.scrollHeight + "px"
                }
            }
        },
        updateLocalValue(event) {
            this.localValue = event
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
        setTimeout(function () {
            app.setTextareaHeight()
        }, 0)
    }
})
</script>

<style scoped lang="less">
pre {
    white-space: pre-wrap;
    word-break: break-all;
}

input.flatpicker-input {
    box-sizing: border-box;
    padding: 0.5rem;
    width: 100%;
}

textarea#editor {
    display: none;
}
</style>
