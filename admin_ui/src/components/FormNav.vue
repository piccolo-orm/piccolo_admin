<template>
    <ul>
        <li v-bind:key="formConfig.name" v-for="formConfig in formConfigs">
            <router-link
                :to="{ name: 'addForm', params: { formSlug: formConfig.slug } }"
                class="subtle"
            >
                <font-awesome-icon icon="level-up-alt" />
                {{ readable(formConfig.name) }}
            </router-link>
        </li>
    </ul>
</template>


<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    computed: {
        formConfigs() {
            return this.$store.state.formConfigs
        },
    },
    methods: {
        readable(value: string) {
            return value.split("_").join(" ")
        },
    },
    async mounted() {
        await this.$store.dispatch("fetchFormConfigs")
    },
})
</script>


<style scoped lang="less">
ul {
    padding: 0;

    li {
        list-style: none;
        text-indent: 0.5rem;
        text-transform: capitalize;

        svg {
            transform: rotate(90deg);
        }
    }
}
</style>
