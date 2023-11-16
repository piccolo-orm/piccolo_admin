<template>
    <a
        class="button"
        @click.prevent="showModal = true"
        data-uitest="csv_button"
    >
        <font-awesome-icon icon="file-csv" />
        <span>{{ $t("Export CSV") }}</span>
    </a>

    <CSVModal v-show="showModal" @close="showModal = false" />
</template>

<script setup lang="ts">
import { ref } from "vue"
import CSVModal from "./CSVModal.vue"

const showModal = ref<boolean>(false)
</script>
