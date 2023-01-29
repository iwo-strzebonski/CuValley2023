/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import pinia from './pinia'
import sweetalert from './sweetalert2'
import vuetify from './vuetify'

// Types
import type Swal from 'sweetalert2'
import type { App } from 'vue'

// Declarations
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $swal: typeof Swal & typeof Swal.fire
  }
}

// Export
export function registerPlugins(app: App) {
  app.use(vuetify)
  app.use(pinia())
  app.use(sweetalert)

  app.mount('#app')
}
