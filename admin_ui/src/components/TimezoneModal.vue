<template>
    <Modal v-on:close="$emit('close')">
        <h1>{{ $t("Timezone") }}</h1>
        <p>
            <!-- prettier-ignore -->
            {{ $t("For timestamps which are timezone aware, they will be displayed in this timezone by default.") }}
        </p>

        <form @submit.prevent="handleSave">
            <select v-model="timezone">
                <option
                    :value="tzName"
                    v-for="tzName in moment.tz.names()"
                    :key="tzName"
                >
                    {{ tzName }}
                </option>
            </select>

            <button>{{ $t("Save") }}</button>

            <p class="note">
                <!-- prettier-ignore -->
                {{ $t("Note: They are converted to UTC when stored in the database.") }}
            </p>
        </form>
    </Modal>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import moment from "moment-timezone"

import Modal from "./Modal.vue"
import { TIMEZONE_KEY } from "@/localStorage"

/*****************************************************************************/
// Refs

const timezone = ref<string>("UTC")

onMounted(() => {
    timezone.value = localStorage.getItem(TIMEZONE_KEY) ?? "UTC"
})

/*****************************************************************************/
// Emits

const emit = defineEmits(["close"])

/*****************************************************************************/
// Save handler

const handleSave = () => {
    localStorage.setItem(TIMEZONE_KEY, timezone.value)
    emit("close")
}
</script>

<style lang="less">
p.note {
    font-size: 0.8em;
}
</style>
