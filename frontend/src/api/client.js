import axios from 'axios'

const client = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api'
})
client.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})


export const setAuthToken = token => {
    if (token) {
        client.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
        delete client.defaults.headers.common['Authorization']
    }
}
export default client
