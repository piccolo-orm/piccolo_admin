<template>
    <div>
        <input
            type="time"
            v-model="localValue"
            :placeholder="placeholder"
            :step="timeResolution"
        />
    </div>
</template>

<script lang="ts" setup>
import moment from "moment"
import { onMounted, type PropType, toRef, ref, watch, computed } from "vue"

/*****************************************************************************/
// Props

const props = defineProps({
    time: {
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

const time = toRef(props, "time")
const timeResolution = toRef(props, "timeResolution")

/*****************************************************************************/
// Events

const emit = defineEmits(["update"])

/*****************************************************************************/
// Refs

const localValue = ref<string>("")

/*****************************************************************************/
// Computed date format

// We dynamically work out the time format based on the time resolution.
const timeFormat = computed(() => {
    var format = "HH:mm"

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
    emit("update", newValue)
})

/*****************************************************************************/

onMounted(() => {
    if (time.value) {
        localValue.value = moment("2000-01-01T" + time.value).format(
            timeFormat.value
        )
    }
})

watch(time, (newValue: string) => {
    if (newValue) {
        localValue.value = moment("2000-01-01T" + time.value).format(
            timeFormat.value
        )
    }
})
</script>

<style lang="less" scoped></style>
