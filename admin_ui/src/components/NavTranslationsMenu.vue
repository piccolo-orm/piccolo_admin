<template>
    <DropDownMenu>
        <li
            v-bind:key="translation.language_code"
            v-for="translation in translations"
        >
            <a
                href="#"
                @click.prevent="updateLanguage(translation.language_code)"
            >
                {{ translation.language_name }}
                <span class="language_code"
                    >({{ translation.language_code }})</span
                >
            </a>
        </li>
    </DropDownMenu>
</template>

<script lang="ts">
import Vue from "vue"
import DropDownMenu from "./DropDownMenu.vue"
import { TranslationListItemAPI } from "@/interfaces"

export default Vue.extend({
    components: {
        DropDownMenu
    },
    methods: {
        async updateLanguage(languageCode: string) {
            await this.$store.dispatch("fetchTranslation", languageCode)
            this.$emit("closeDropdown", false)
        }
    },
    computed: {
        translations(): TranslationListItemAPI[] {
            return this.$store.state.translationsModule.translations
        }
    }
})
</script>

<style scoped lang="less">
li {
    a {
        text-transform: capitalize;

        span.language_code {
            text-transform: lowercase;
        }
    }
}
</style>
