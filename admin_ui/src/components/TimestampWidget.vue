<template>
    <div>
        <input
            type="datetime-local"
            v-model="localValue"
            :placeholder="placeholder"
            :step="timeResolution"
        />
    </div>
</template>

<script lang="ts" setup>
import moment from "moment-timezone"
import { onMounted, type PropType, toRef, ref, watch, computed } from "vue"

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
    emit("update", newValue)
})

/*****************************************************************************/

onMounted(() => {
    if (datetime.value) {
        localValue.value = moment(datetime.value).format(datetimeFormat.value)
    }
})

watch(datetime, (newValue: string) => {
    if (newValue) {
        localValue.value = moment(datetime.value).format(datetimeFormat.value)
    }
})
</script>

<style lang="less" scoped></style>
