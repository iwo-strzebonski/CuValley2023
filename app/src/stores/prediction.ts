import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

const usePredictionStore = defineStore('prediction', () => {
  const data = ref<any>({})
  const labels = ref<string[]>([])

  const getData = async (meteoFile: File, hydroFile: File) => {
    const axiosClient = axios.create({
      baseURL: '/api',
      headers: {
        'Content-Type': 'multipart/form-data',
        'Accept': 'application/json'
      }
    })

    data.value = [0, 1, 2, 3, 5, 0]

    const formData = new FormData()
    formData.append('meteo_file', meteoFile, meteoFile.name)
    formData.append('hydro_file', hydroFile, hydroFile.name)

    const response = await axiosClient.post('/forecast', formData)

    console.debug(Object.values(response.data))

    data.value = {
      label: 'Water Level',
      data: Object.values(response.data),
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1
    }

    labels.value = Object.keys(response.data)
  }

  return {
    data,
    labels,
    getData
  }
})

export default usePredictionStore
