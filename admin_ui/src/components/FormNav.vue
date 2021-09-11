<template>
    <ul>
        <li
            v-bind:key="formName"
            v-for="formName in formNames"
        >
            <router-link
                :to="{ name: 'addForm', params: { formName } }"
                class="subtle"
            >
                <font-awesome-icon icon="level-up-alt" />
                {{ formName | readable }}
            </router-link>
        </li>
    </ul>
</template>


<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        formNames() {
            return this.$store.state.formNames
        },
        currentFormName() {
            return this.$store.state.currentFormName
        },
    },
    methods: {
        showListing(formName: string) {
            this.$store.commit("updateCurrentFormname", formName)
            this.$router.push({ name: "formAdding", params: { formName } })
        },
    },
    async mounted() {
        await this.$store.dispatch("fetchFormNames")
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
