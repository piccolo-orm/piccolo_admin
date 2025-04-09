import { createI18n } from "vue-i18n"

const i18n = createI18n({
    locale: "en",
    silentTranslationWarn: import.meta.env.PROD
})

export default i18n
