import '@fontsource/roboto'
import '@sweetalert2/theme-dark/dark.css'
import { createApp } from 'vue'
import 'vue3-treeview/dist/style.css'

import '@/@types/globals.d'
import App from '@/App.vue'
import { registerPlugins } from '@/plugins'
import '@/styles/main.css'

const app = createApp(App)
registerPlugins(app)
