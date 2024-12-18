import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // Altere para o endereço do seu servidor
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
