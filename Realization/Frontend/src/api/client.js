import axios from 'axios'

// Создаем экземпляр axios с базовой конфигурацией
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor для обработки ошибок
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

/**
 * API методы для взаимодействия с бэкендом
 */
export const api = {
  /**
   * Предсказание тональности для одного текста
   * @param {string} text - Текст для анализа
   * @returns {Promise} Результат предсказания
   */
  async predictSingle(text) {
    const response = await apiClient.post('/predict', { text })
    return response.data
  },

  /**
   * Предсказание тональности для нескольких текстов
   * @param {string[]} texts - Массив текстов для анализа
   * @returns {Promise} Массив результатов
   */
  async predictBatch(texts) {
    const response = await apiClient.post('/predict/batch', { texts })
    return response.data
  },

  /**
   * Запуск обучения модели
   * @param {boolean} force - Принудительное переобучение
   * @param {boolean} spark - Использовать Spark для обработки данных
   * @returns {Promise} Статус запуска обучения
   */
  async startTraining(force = false, spark = false) {
    const response = await apiClient.post('/train', null, {
      params: { force, spark }
    })
    return response.data
  },

  /**
   * Получение статуса обучения
   * @returns {Promise} Статус обучения
   */
  async getTrainingStatus() {
    const response = await apiClient.get('/train/status')
    return response.data
  },

  /**
   * Проверка здоровья системы
   * @returns {Promise} Статус системы
   */
  async checkHealth() {
    const response = await apiClient.get('/health')
    return response.data
  },

  /**
   * Скачивание модели
   * @returns {Promise} Файл модели
   */
  async downloadModel() {
    const response = await apiClient.get('/download/model', {
      responseType: 'blob'
    })
    return response.data
  },

  /**
   * Скачивание словаря
   * @returns {Promise} Файл словаря
   */
  async downloadVocab() {
    const response = await apiClient.get('/download/vocab', {
      responseType: 'blob'
    })
    return response.data
  }
}

export default api

