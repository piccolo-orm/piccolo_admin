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

const countDecimalPlaces = (value: number) => {
    var text = value.toString()
    var index = text.indexOf(".")
    return index == -1 ? 0 : text.length - index - 1
}

// We dynamically work out the datetime format based on the time resolution.
const datetimeFormat = computed(() => {
    var format = "YYYY-MM-DDTHH:mm"

    if (timeResolution.value < 60) {
        format += ":ss"
    }

    if (timeResolution.value < 1) {
        let decimalPlaces = countDecimalPlaces(timeResolution.value)

        // We can't allow more than 3 decimal places, as milliseconds is the
        // max resolution.
        decimalPlaces = decimalPlaces > 3 ? 3 : decimalPlaces

        format += "."

        Array.from(Array(decimalPlaces)).forEach(() => {
            format += "S"
        })
    }
    return format
})

/*****************************************************************************/
// Handle updates

watch(localValue, (newValue) => {
    const value = moment.tz(newValue, timezone.value).toISOString()
    console.log(`Emit update ${value}`)
    emit("update", value)
})

// When the timezone is changed, we change the displayed datetime so it matches
// the newly selected timezone.
watch(timezone, (newTimezoneValue) => {
    localValue.value = moment
        .tz(datetime.value, newTimezoneValue)
        .format(datetimeFormat.value)
})

/*****************************************************************************/

onMounted(() => {
    if (datetime.value) {
        const value = moment
            .tz(datetime.value, timezone.value)
            .format(datetimeFormat.value)
        console.log(value)
        localValue.value = value
    }
})

watch(datetime, (newValue: string) => {
    if (newValue) {
        const value = moment
            .tz(newValue, timezone.value)
            .format(datetimeFormat.value)
        console.log(`datetime prop changed - ${value}`)
        localValue.value = value
    }
})
</script>

<style lang="less" scoped></style>
