import '../src/fontawesome'
import Vue from 'vue'


export const decorators = [(story) => ({
  components: {
    'router-link': Vue.component('router-link', { template: '<a href="">Link</a>' })
  },
  template: `<story />`,
})];


export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
}