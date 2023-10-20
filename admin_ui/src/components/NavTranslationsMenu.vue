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
                <font-awesome-icon
                    v-if="currentLanguageCode == translation.language_code"
                    icon="check"
                />

                {{ translation.language_name }}
                <span class="language_code"
                    >({{ translation.language_code }})</span
                >
            </a>
        </li>
    </DropDownMenu>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import DropDownMenu from "./DropDownMenu.vue"
import type { TranslationListItemAPI } from "@/interfaces"

export default defineComponent({
    components: {
        DropDownMenu
    },
    methods: {
        async updateLanguage(languageCode: string) {
            await this.$store.dispatch("loadTranslation", languageCode)
            this.$emit("closeDropdown", false)
        }
    },
    computed: {
        translations(): TranslationListItemAPI[] {
            return this.$store.state.translationsModule.translations
        },
        currentLanguageCode(): string {
            return this.$i18n.locale || "en"
        }
    }
})
</script>

<style scoped lang="less">
li {
    a {
        text-transform: capitalize;

        span.language_code {
            text-transform: initial;
        }
    }
}
</style>
