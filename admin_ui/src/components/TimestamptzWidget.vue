<template>
    <div>
        <input
            type="datetime-local"
            v-model="localValue"
            :placeholder="placeholder"
            :step="timeResolution"
        />

        <select v-model="timezone">
            <option
                :value="tzName"
                v-for="tzName in moment.tz.names()"
                :key="tzName"
            >
                {{ tzName }}
            </option>
        </select>
    </div>
</template>

<script lang="ts" setup>
import moment from "moment-timezone"
import { onMounted, type PropType, toRef, ref, watch, computed } from "vue"

import { TIMEZONE_KEY } from "@/localStorage"

/*****************************************************************************/
// Props

const props = defineProps({
    datetime: {
        type: undefined as any as PropType<string>,
        required: true
    },
    placeholder: {
        type: String as PropType<string>,
        required: true
    },
    timeResolution: {
        type: Number as PropType<number>,
        default: 60
    }
})

const datetime = toRef(props, "datetime")
const timeResolution = toRef(props, "timeResolution")

/*****************************************************************************/
// Events

const emit = defineEmits(["update"])

/*****************************************************************************/
// Refs

const localValue = ref<string>("")
const timezone = ref<string>(localStorage.getItem(TIMEZONE_KEY) ?? "UTC")

/*****************************************************************************/
// Computed date format

// We dynamically work out the datetime format based on the time resolution.
const datetimeFormat = computed(() => {
    var format = "YYYY-MM-DDTHH:mm"

    if (timeResolution.value < 60) {
        format += ":ss"
    }

    if (timeResolution.value < 1) {
        format += ".SSS"
    }

    return format
})

/*****************************************************************************/
// Handle updates

watch(localValue, (newValue) => {
    emit("update", moment.tz(newValue, timezone.value).toISOString())
})

// When the timezone is changed, we change the displayed datetime so it matches
// the newly selected timezone.
watch(timezone, (newTimezoneValue) => {
    if (datetime.value) {
        localValue.value = moment
            .tz(datetime.value, newTimezoneValue)
            .format(datetimeFormat.value)
    }
})

/*****************************************************************************/

onMounted(() => {
    if (datetime.value) {
        localValue.value = moment
            .tz(datetime.value, timezone.value)
            .format(datetimeFormat.value)
    }
})

watch(datetime, (newValue: string) => {
    if (newValue) {
        localValue.value = moment
            .tz(newValue, timezone.value)
            .format(datetimeFormat.value)
    }
})
</script>

<style lang="less" scoped></style>
