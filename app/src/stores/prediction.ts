import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'

const usePredictionStore = defineStore('prediction', () => {
  const data = ref<any>([])
  const labels = ref<string[]>(['1', '2', '3', '4', '5', '6'])

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

    console.debug(response.data)

    // data.value = response.data
  }

  return {
    data,
    labels,
    getData
  }
})

export default usePredictionStore
