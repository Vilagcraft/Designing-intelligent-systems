<template>
  <el-card class="predict-batch-card">
    <template #header>
      <div class="card-header">
        <span>Пакетный анализ тональности</span>
      </div>
    </template>

    <el-form>
      <el-form-item>
        <template #label>
          <span>Введите тексты (каждый с новой строки):</span>
          <el-text type="info" size="small" style="margin-left: 10px;">
            {{ texts.length }} текст(ов)
          </el-text>
        </template>
        <el-input
          v-model="inputTexts"
          type="textarea"
          :rows="10"
          placeholder="Первый текст&#10;Второй текст&#10;Третий текст&#10;..."
          :disabled="loading"
        />
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          @click="handleBatchPredict"
          :loading="loading"
          :disabled="texts.length === 0"
        >
          <el-icon class="el-icon--left"><Search /></el-icon>
          Анализировать все ({{ texts.length }})
        </el-button>
        <el-button @click="handleClear" :disabled="loading">
          Очистить
        </el-button>
      </el-form-item>
    </el-form>

    <!-- Результаты -->
    <el-divider v-if="results.length > 0" />

    <div v-if="results.length > 0" class="results-container">
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="📊 Аналитика" name="analytics">
          <Analytics :results="results" />
        </el-tab-pane>
        
        <el-tab-pane label="📋 Таблица результатов" name="table">
      <div class="results-header">
        <h3>Результаты анализа:</h3>
        <el-space>
          <el-statistic title="Всего" :value="results.length" />
          <el-statistic 
            title="Успешно" 
            :value="successCount"
            :value-style="{ color: '#67c23a' }"
          />
          <el-statistic 
            v-if="errorCount > 0"
            title="Ошибок" 
            :value="errorCount"
            :value-style="{ color: '#f56c6c' }"
          />
        </el-space>
      </div>

      <el-table 
        :data="results" 
        style="width: 100%; margin-top: 20px"
        stripe
        border
      >
        <el-table-column type="index" label="#" width="60" />
        
        <el-table-column label="Текст" min-width="300">
          <template #default="scope">
            <el-text :line-clamp="2">{{ scope.row.text }}</el-text>
          </template>
        </el-table-column>
        
        <el-table-column label="Тональность" width="150" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.label" :type="getTagType(scope.row.label)">
              {{ getLabelText(scope.row.label) }}
            </el-tag>
            <el-tag v-else type="danger">Ошибка</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="Статус" width="120" align="center">
          <template #default="scope">
            <el-icon v-if="scope.row.label" color="#67c23a" :size="20">
              <SuccessFilled />
            </el-icon>
            <el-tooltip v-else :content="scope.row.error" placement="top">
              <el-icon color="#f56c6c" :size="20">
                <CircleCloseFilled />
              </el-icon>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <div class="export-section">
        <el-button @click="exportResults" type="success">
          <el-icon class="el-icon--left"><Download /></el-icon>
          Экспортировать результаты (JSON)
        </el-button>
      </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElNotification } from 'element-plus'
import { Search, Download, SuccessFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import api from '../api/client'
import Analytics from './Analytics.vue'

const inputTexts = ref('')
const results = ref([])
const loading = ref(false)
const activeTab = ref('analytics')

const texts = computed(() => {
  return inputTexts.value
    .split('\n')
    .map(text => text.trim())
    .filter(text => text.length > 0)
})

const successCount = computed(() => {
  return results.value.filter(r => r.label).length
})

const errorCount = computed(() => {
  return results.value.filter(r => r.error).length
})

const handleBatchPredict = async () => {
  if (texts.value.length === 0) return

  loading.value = true
  results.value = []

  try {
    const response = await api.predictBatch(texts.value)
    results.value = response.results
    
    const successMsg = `Обработано: ${successCount.value} из ${results.value.length}`
    
    ElNotification({
      title: 'Анализ завершен',
      message: successMsg,
      type: successCount.value === results.value.length ? 'success' : 'warning',
      duration: 3000
    })
  } catch (err) {
    ElNotification({
      title: 'Ошибка',
      message: err.response?.data?.detail || err.message || 'Произошла ошибка при анализе',
      type: 'error',
      duration: 3000
    })
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  inputTexts.value = ''
  results.value = []
}

const getTagType = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive') || labelLower.includes('положительн')) return 'success'
  if (labelLower.includes('negative') || labelLower.includes('отрицательн')) return 'danger'
  return 'info'
}

const getLabelText = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive')) return 'Положительная'
  if (labelLower.includes('negative')) return 'Отрицательная'
  if (labelLower.includes('neutral')) return 'Нейтральная'
  return label
}

const exportResults = () => {
  const dataStr = JSON.stringify(results.value, null, 2)
  const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr)
  
  const exportFileDefaultName = `sentiment-results-${Date.now()}.json`
  
  const linkElement = document.createElement('a')
  linkElement.setAttribute('href', dataUri)
  linkElement.setAttribute('download', exportFileDefaultName)
  linkElement.click()
  
  ElNotification({
    title: 'Экспорт',
    message: 'Результаты экспортированы',
    type: 'success',
    duration: 2000
  })
}
</script>

<style scoped>
.predict-batch-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.results-container {
  margin-top: 20px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

h3 {
  margin: 0;
  color: var(--el-text-color-primary);
}

.export-section {
  margin-top: 20px;
  text-align: right;
}
</style>

