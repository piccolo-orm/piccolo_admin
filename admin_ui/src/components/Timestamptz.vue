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
import { onMounted, type PropType, toRef, ref, watch } from "vue"

import { TIMEZONE_KEY } from "@/localStorage"

const DATE_TIME_FORMAT = "YYYY-MM-DDTHH:mm:ss.SSS"

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
        default: 1
    }
})

const datetime = toRef(props, "datetime")

/*****************************************************************************/
// Events

const emit = defineEmits(["update"])

/*****************************************************************************/
// Refs

const localValue = ref<string>("")
const timezone = ref<string>(localStorage.getItem(TIMEZONE_KEY) ?? "UTC")

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
        .format(DATE_TIME_FORMAT)
})

/*****************************************************************************/

onMounted(() => {
    if (datetime.value) {
        const value = moment
            .tz(datetime.value, timezone.value)
            .format(DATE_TIME_FORMAT)
        console.log(value)
        localValue.value = value
    }
})

watch(datetime, (newValue: string) => {
    if (newValue) {
        const value = moment
            .tz(newValue, timezone.value)
            .format(DATE_TIME_FORMAT)
        console.log(`datetime prop changed - ${value}`)
        localValue.value = value
    }
})
</script>

<style lang="less" scoped></style>
