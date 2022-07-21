import Vue from "vue"
import VueI18n from "vue-i18n"

Vue.use(VueI18n)

const i18n = new VueI18n({
    locale: "en",
    silentTranslationWarn: process.env.NODE_ENV === "production"
})

export default i18n
