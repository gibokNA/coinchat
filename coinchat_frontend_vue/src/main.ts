import { createApp } from 'vue'
import { createPinia } from 'pinia'
import mitt from 'mitt'

import App from './App.vue'
import router from './router'

import axios from 'axios'
import VueAxios from 'vue-axios'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

const app = createApp(App)

const eventBus = mitt();

app.use(VueAxios, axios)
app.provide('axios', app.config.globalProperties.axios) // provide 'axios'

app.use(createPinia())
app.use(router)

app.provide('eventBus', eventBus);

app.mount('#app')
