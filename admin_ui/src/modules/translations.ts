import axios from "axios"

import i18n from "@/translations"
import type {
    TranslationsListAPIResponse,
    TranslationListItemAPI,
    TranslationAPIResponse
} from "@/interfaces"
import type { Context } from "./interfaces"

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

interface State {
    translations: TranslationListItemAPI[]
}

export default {
    state: {
        translations: []
    } as State,
    mutations: {
        updateTranslations(state: State, value: TranslationListItemAPI[]) {
            state.translations = value
        }
    },
    actions: {
        async setupTranslations(context: Context) {
            // This fetches a list of all available translations (not the
            // translations themselves):
            const response = await axios.get<TranslationsListAPIResponse>(
                `./public/translations/`
            )
            const data = response.data
            context.commit("updateTranslations", data.translations)

            const availableLanguageCodes = data.translations.map(
                (translation) => {
                    return translation.language_code.toLowerCase()
                }
            )

            let defaultLanguage: string | null = null

            // If the user has previously used the app, and set their default
            // language, then load it from localStorage:
            const storedLanguagePreference =
                localStorageUtils.getDefaultLanguage()

            if (
                storedLanguagePreference &&
                availableLanguageCodes.indexOf(storedLanguagePreference) != -1
            ) {
                defaultLanguage = storedLanguagePreference
            } else {
                if (data.default_language_code == "auto") {
                    // Fetch the user's language preference from the browser.

                    // Make it lowercase so it's consistent across browsers:
                    const browserLanguage = navigator.language.toLowerCase()

                    if (availableLanguageCodes.indexOf(browserLanguage) != -1) {
                        defaultLanguage = browserLanguage
                    } else {
                        // Language codes can either be like 'en' or 'en-US'. If
                        // we don't have a language available for 'en-US', then
                        // check if we have 'en' instead.
                        const _browserLanguage = browserLanguage.split("-")[0]

                        if (
                            availableLanguageCodes.indexOf(_browserLanguage) !=
                            -1
                        ) {
                            defaultLanguage = _browserLanguage
                        }
                    }
                } else {
                    defaultLanguage = data.default_language_code
                }
            }

            await context.dispatch("loadTranslation", defaultLanguage || "en")
        },
        /**
         * Fetch the translations for a certain language, and store it.
         */
        async loadTranslation(context: Context, languageCode: string) {
            const response = await axios.get<TranslationAPIResponse>(
                `./public/translations/${languageCode}/`
            )
            localStorageUtils.setDefaultLanguage(languageCode)

            i18n.global.setLocaleMessage(
                response.data.language_code,
                response.data.translations
            )
            i18n.global.locale = response.data.language_code
        }
    }
}
