import axios from "axios"

import {
    TranslationsListAPIResponse,
    TranslationListItemAPI,
    TranslationAPIResponse
} from "@/interfaces"
import i18n from "@/i18n"

const DEFAULT_LANGUAGE_KEY = "piccoloAdminDefaultLanguage"

/**
 * Stores the user's default language in localStorage. If the user selects a
 * language, then this becomes their new default language, otherwise it's
 * defined by the API.
 */
const localStorageUtils = {
    getDefaultLanguage: (): string | null => {
        return localStorage.getItem(DEFAULT_LANGUAGE_KEY)
    },
    setDefaultLanguage: (value: string) => {
        return localStorage.setItem(DEFAULT_LANGUAGE_KEY, value)
    }
}

export default {
    state: {
        defaultLanguage: null as string | null,
        translations: null as string | TranslationListItemAPI[]
    },
    mutations: {
        updateDefaultLanguage(state, value: string) {
            state.defaultLanguage = value
        },
        updateTranslations(state, value: object) {
            state.translations = value
        }
    },
    actions: {
        /**
         * This fetches a list of all available translations (not the
         * translations themselves).
         */
        async fetchTranslations(context) {
            const response = await axios.get<TranslationsListAPIResponse>(
                `./public/translations/`
            )

            context.commit("updateTranslations", response.data.translations)

            if (!context.state.defaultLanguage) {
                context.commit(
                    "updateDefaultLanguage",
                    response.data.default_language_code
                )
            }
        },
        /**
         * Fetch the translations for a certain language.
         */
        async fetchTranslation(context, languageCode: string) {
            const response = await axios.get<TranslationAPIResponse>(
                `./public/translations/${languageCode}/`
            )
            i18n.setLocaleMessage(
                response.data.language_code,
                response.data.translations
            )
            i18n.locale = response.data.language_code
        },
        /**
         * If the user has previously used the app, and set their default
         * language, then load it from localStorage.
         */
        async loadDefaultLanguage(context) {
            const defaultLanguage = localStorageUtils.getDefaultLanguage()
            if (defaultLanguage) {
                context.commit("updateDefaultLanguage", defaultLanguage)
            }
        }
    }
}
