import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import { VBtn } from 'vuetify/components'
import 'vuetify/styles'

export default createVuetify({
  aliases: {
    VBtnAlt: VBtn
  },
  // https://next.vuetifyjs.com/features/global-configuration/
  defaults: {
    global: {
      rounded: 'sm'
    },
    VAppBar: {
      flat: true
    },
    VBtn: {
      color: 'primary',
      height: 44,
      minWidth: 190
    },
    VBtnAlt: {
      color: 'primary',
      height: 48,
      minWidth: 190,
      variant: 'outlined'
    },
    VSheet: {
      color: '#212121'
    }
  },
  // https://next.vuetifyjs.com/features/theme/
  theme: {
    defaultTheme: 'dark',
    // defaultTheme: 'light',
    themes: {
      dark: {
        dark: true,
        colors: {
          primary: '#1697f6'
        }
      }
    }
  }
})
