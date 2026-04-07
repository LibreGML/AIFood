/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from './vuetify'
import router from '@/router'
import apiClient from './axios'

export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(router)
    .provide('$http', apiClient)
}