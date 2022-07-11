<template>
    <DropDownMenu>
        <li v-bind:key="key" v-for="(property, key) in $root.$i18n.messages">
            <a
                href="#"
                v-on:click="
                    $root.$i18n.locale = key
                    closeDropdown()
                    getTranslation(key)
                "
            >
                {{ key }}
            </a>
        </li>
    </DropDownMenu>
</template>

<script lang="ts">
import Vue from "vue"
import axios from "axios"
import DropDownMenu from "./DropDownMenu.vue"

export default Vue.extend({
    props: {
        showLanguageDropdown: Boolean
    },
    components: {
        DropDownMenu
    },
    methods: {
        closeDropdown() {
            this.$emit("closeDropdown", false)
        },
        async getTranslation(value) {
            const response = await axios.get(`./api/languages/${value}`)
            return response.data
        }
    }
})
</script>

<style scoped lang="less">
a::first-letter {
    text-transform: capitalize;
}
</style>
