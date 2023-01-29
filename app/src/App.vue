<script lang="ts">
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale
} from 'chart.js'
import 'chartjs-adapter-moment'
import { Line } from 'vue-chartjs'

import usePredictionStore from '@/stores/prediction'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement, TimeScale)
export default {
  name: 'KGHMFrontend',
  components: {
    LineChart: Line
  },
  setup() {
    const store = usePredictionStore()

    return {
      store
    }
  },
  methods: {
    async getData() {
      const data = await this.$swal.fire({
        title: 'Welcome to KGHM Frontend!',
        html:
          '<input type="file" id="swal-input1" class="swal2-input" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">' +
          '<label for="swal-input1">Choose meteo file...</label>' +
          '<input type="file" id="swal-input2" class="swal2-input" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">' +
          '<label for="swal-input2">Choose hydro file...</label>',
        confirmButtonText: 'OK',
        focusConfirm: true,
        preConfirm: () => {
          const meteoInput = document.getElementById('swal-input1') as HTMLInputElement
          const hydroInput = document.getElementById('swal-input2') as HTMLInputElement

          if (!(meteoInput.files && meteoInput.files[0] && hydroInput.files && hydroInput.files[0])) {
            this.$swal.showValidationMessage('Please choose files')
            return
          }

          return { meteoFile: meteoInput.files[0], hydroFile: hydroInput.files[0] }
        }
      })

      if (!(data.isConfirmed && data.value)) return

      console.debug(data.value.meteoFile, data.value.hydroFile)

      await this.store.getData(data.value.meteoFile, data.value.hydroFile)
    }
  },
  async mounted() {
    this.$swal({
      title: 'Welcome to KGHM Frontend!',
      text: 'This is a web application for predicting the water level of the Odra River.',
      icon: 'info',
      confirmButtonText: 'OK'
    })
  }
}
</script>

<template>
  <v-app>
    <v-main>
      <h1>KGHM Frontend</h1>
      <v-card v-if="!Object.keys(store.data).length">
        Waiting for data...
        <v-btn @click="getData">Load data</v-btn>
      </v-card>
      <line-chart v-else :data="{ datasets: store.data, labels: store.labels }" />
    </v-main>
  </v-app>
</template>
