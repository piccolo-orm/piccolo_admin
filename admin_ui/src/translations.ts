import { createI18n } from "vue-i18n"

const i18n = createI18n({
    locale: "en",
    silentTranslationWarn: process.env.NODE_ENV === "production"
})

export default i18n
