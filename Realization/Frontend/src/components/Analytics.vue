<template>
  <el-card class="analytics-card">
    <template #header>
      <div class="card-header">
        <span>📊 Аналитика и визуализация</span>
        <el-tag type="info">{{ results.length }} текст(ов)</el-tag>
      </div>
    </template>

    <el-empty v-if="results.length === 0" description="Нет данных для отображения">
      <el-button type="primary" @click="$emit('analyze')">
        Начать анализ
      </el-button>
    </el-empty>

    <div v-else class="analytics-content">
      <!-- Основная статистика -->
      <el-row :gutter="20" class="stats-row">
        <el-col :xs="12" :sm="6">
          <el-statistic title="Всего текстов" :value="results.length">
            <template #prefix>
              <el-icon><Document /></el-icon>
            </template>
          </el-statistic>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-statistic 
            title="Положительных" 
            :value="positiveCount"
            :value-style="{ color: '#67c23a' }"
          >
            <template #prefix>
              <el-icon><CircleCheck /></el-icon>
            </template>
          </el-statistic>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-statistic 
            title="Отрицательных" 
            :value="negativeCount"
            :value-style="{ color: '#f56c6c' }"
          >
            <template #prefix>
              <el-icon><CircleClose /></el-icon>
            </template>
          </el-statistic>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-statistic 
            title="Нейтральных" 
            :value="neutralCount"
            :value-style="{ color: '#909399' }"
          >
            <template #prefix>
              <el-icon><Minus /></el-icon>
            </template>
          </el-statistic>
        </el-col>
      </el-row>

      <el-divider />

      <!-- Графики первого ряда -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="8">
          <SentimentGaugeChart 
            :value="averageConfidence"
            title="Средняя уверенность"
          />
        </el-col>
        <el-col :xs="24" :md="16">
          <SentimentPieChart 
            :data="results"
            title="Распределение тональности"
          />
        </el-col>
      </el-row>

      <el-divider />

      <!-- Графики второго ряда -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <SentimentBarChart 
            :data="results"
            title="Количество по категориям"
          />
        </el-col>
        <el-col :xs="24" :md="12">
          <TextLengthHistogram 
            :data="results"
            title="Распределение длины текстов"
          />
        </el-col>
      </el-row>

      <el-divider />

      <!-- Статистика по языкам (если доступна) -->
      <div v-if="hasLanguages" class="language-stats">
        <h3>Распределение по языкам</h3>
        <el-row :gutter="20">
          <el-col :xs="24" :md="12">
            <el-card shadow="hover">
              <template #header>
                <span>🌐 Круговая диаграмма языков</span>
              </template>
              <div ref="languagePieRef" style="width: 100%; height: 300px;"></div>
            </el-card>
          </el-col>
          <el-col :xs="24" :md="12">
            <el-card shadow="hover">
              <template #header>
                <span>📊 Таблица языков</span>
              </template>
              <el-table :data="languageStats" stripe style="width: 100%">
                <el-table-column prop="language" label="Язык" width="120">
                  <template #default="scope">
                    <el-tag type="primary">{{ getLanguageText(scope.row.language) }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="count" label="Количество" width="100" align="center" />
                <el-table-column prop="percentage" label="Процент" align="center">
                  <template #default="scope">
                    {{ scope.row.percentage }}%
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <el-divider v-if="hasLanguages" />

      <!-- Статистика по рейтингам (если доступна) -->
      <div v-if="hasRatings" class="rating-stats">
        <h3>Распределение рейтингов</h3>
        <el-row :gutter="20">
          <el-col :xs="24" :md="12">
            <el-card shadow="hover">
              <template #header>
                <span>⭐ Гистограмма рейтингов</span>
              </template>
              <div ref="ratingHistogramRef" style="width: 100%; height: 300px;"></div>
            </el-card>
          </el-col>
          <el-col :xs="24" :md="12">
            <el-card shadow="hover">
              <template #header>
                <span>📈 Средний рейтинг по тональности</span>
              </template>
              <div ref="ratingBySentimentRef" style="width: 100%; height: 300px;"></div>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px;">
          <el-col :xs="12" :sm="6">
            <el-statistic title="Средний рейтинг" :value="averageRating" :precision="2">
              <template #prefix>
                <el-icon><Star /></el-icon>
              </template>
            </el-statistic>
          </el-col>
          <el-col :xs="12" :sm="6">
            <el-statistic 
              title="Макс. рейтинг" 
              :value="maxRating"
              :value-style="{ color: '#67c23a' }"
            />
          </el-col>
          <el-col :xs="12" :sm="6">
            <el-statistic 
              title="Мин. рейтинг" 
              :value="minRating"
              :value-style="{ color: '#f56c6c' }"
            />
          </el-col>
          <el-col :xs="12" :sm="6">
            <el-statistic title="С рейтингом" :value="ratingsCount" />
          </el-col>
        </el-row>
      </div>

      <el-divider v-if="hasRatings" />

      <!-- Графики третьего ряда -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <ConfidenceChart 
            :data="results"
            title="График уверенности модели"
          />
        </el-col>
        <el-col :xs="24" :md="12">
          <SentimentRadarChart 
            :data="results"
            title="Многомерный анализ"
          />
        </el-col>
      </el-row>

      <!-- Детальная таблица статистики -->
      <el-divider content-position="left">Детальная статистика</el-divider>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="Всего проанализировано">
          {{ results.length }} текстов
        </el-descriptions-item>
        <el-descriptions-item label="Успешных анализов">
          {{ successCount }} ({{ successRate }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Средняя длина текста">
          {{ averageLength }} символов
        </el-descriptions-item>
        <el-descriptions-item label="Средняя уверенность">
          {{ (averageConfidence * 100).toFixed(2) }}%
        </el-descriptions-item>
        <el-descriptions-item label="Положительных">
          {{ positiveCount }} ({{ positivePercent }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Отрицательных">
          {{ negativeCount }} ({{ negativePercent }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Нейтральных">
          {{ neutralCount }} ({{ neutralPercent }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Преобладающая тональность">
          <el-tag :type="dominantSentimentType">
            {{ dominantSentiment }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="hasLanguages" label="Языков обнаружено">
          {{ uniqueLanguagesCount }}
        </el-descriptions-item>
        <el-descriptions-item v-if="hasRatings" label="Средний рейтинг">
          {{ averageRating.toFixed(2) }} / 5.0
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </el-card>
</template>

<script setup>
import { computed, ref, watch, nextTick, onMounted, onUnmounted, inject } from 'vue'
import { Document, CircleCheck, CircleClose, Minus, Star } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import SentimentPieChart from './charts/SentimentPieChart.vue'
import SentimentBarChart from './charts/SentimentBarChart.vue'
import ConfidenceChart from './charts/ConfidenceChart.vue'
import TextLengthHistogram from './charts/TextLengthHistogram.vue'
import SentimentRadarChart from './charts/SentimentRadarChart.vue'
import SentimentGaugeChart from './charts/SentimentGaugeChart.vue'

// Refs для дополнительных графиков
const languagePieRef = ref(null)
const ratingHistogramRef = ref(null)
const ratingBySentimentRef = ref(null)
let languagePieChart = null
let ratingHistogramChart = null
let ratingBySentimentChart = null

const props = defineProps({
  results: {
    type: Array,
    default: () => []
  }
})

// Получаем информацию о текущей теме
const isDark = inject('isDark', ref(false))

const positiveCount = computed(() => {
  return props.results.filter(r => 
    r.label?.toLowerCase().includes('positive')
  ).length
})

const negativeCount = computed(() => {
  return props.results.filter(r => 
    r.label?.toLowerCase().includes('negative')
  ).length
})

const neutralCount = computed(() => {
  return props.results.filter(r => 
    r.label?.toLowerCase().includes('neutral')
  ).length
})

const successCount = computed(() => {
  return props.results.filter(r => r.label && !r.error).length
})

const successRate = computed(() => {
  if (props.results.length === 0) return 0
  return ((successCount.value / props.results.length) * 100).toFixed(1)
})

const averageLength = computed(() => {
  if (props.results.length === 0) return 0
  const total = props.results.reduce((sum, r) => sum + (r.text?.length || 0), 0)
  return Math.round(total / props.results.length)
})

const averageConfidence = computed(() => {
  if (successCount.value === 0) return 0
  const total = props.results.reduce((sum, r) => {
    if (r.label && !r.error) {
      // Пытаемся получить уверенность из разных источников
      let confidence = 0
      if (r.confidence !== undefined) {
        confidence = r.confidence
      } else if (r.probs && Array.isArray(r.probs) && r.probs.length > 0) {
        confidence = Math.max(...r.probs)
      }
      return sum + confidence
    }
    return sum
  }, 0)
  return successCount.value > 0 ? total / successCount.value : 0
})

const positivePercent = computed(() => {
  if (props.results.length === 0) return 0
  return ((positiveCount.value / props.results.length) * 100).toFixed(1)
})

const negativePercent = computed(() => {
  if (props.results.length === 0) return 0
  return ((negativeCount.value / props.results.length) * 100).toFixed(1)
})

const neutralPercent = computed(() => {
  if (props.results.length === 0) return 0
  return ((neutralCount.value / props.results.length) * 100).toFixed(1)
})

const dominantSentiment = computed(() => {
  const max = Math.max(positiveCount.value, negativeCount.value, neutralCount.value)
  if (max === positiveCount.value) return 'Положительная'
  if (max === negativeCount.value) return 'Отрицательная'
  return 'Нейтральная'
})

const dominantSentimentType = computed(() => {
  const max = Math.max(positiveCount.value, negativeCount.value, neutralCount.value)
  if (max === positiveCount.value) return 'success'
  if (max === negativeCount.value) return 'danger'
  return 'info'
})

// Вычисляемые свойства для языков
const hasLanguages = computed(() => {
  return props.results.some(r => r.language)
})

const uniqueLanguagesCount = computed(() => {
  const languages = new Set()
  props.results.forEach(r => {
    if (r.language) languages.add(r.language)
  })
  return languages.size
})

const languageStats = computed(() => {
  const stats = {}
  let total = 0
  
  props.results.forEach(r => {
    if (r.language) {
      stats[r.language] = (stats[r.language] || 0) + 1
      total++
    }
  })
  
  return Object.entries(stats)
    .map(([language, count]) => ({
      language,
      count,
      percentage: ((count / total) * 100).toFixed(1)
    }))
    .sort((a, b) => b.count - a.count)
})

// Вычисляемые свойства для рейтингов
const hasRatings = computed(() => {
  return props.results.some(r => r.rating !== undefined && r.rating !== null)
})

const ratingsCount = computed(() => {
  return props.results.filter(r => r.rating !== undefined && r.rating !== null).length
})

const averageRating = computed(() => {
  const ratings = props.results.filter(r => r.rating).map(r => r.rating)
  if (ratings.length === 0) return 0
  return ratings.reduce((sum, r) => sum + r, 0) / ratings.length
})

const maxRating = computed(() => {
  const ratings = props.results.filter(r => r.rating).map(r => r.rating)
  return ratings.length > 0 ? Math.max(...ratings) : 0
})

const minRating = computed(() => {
  const ratings = props.results.filter(r => r.rating).map(r => r.rating)
  return ratings.length > 0 ? Math.min(...ratings) : 0
})

const ratingDistribution = computed(() => {
  const dist = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
  props.results.forEach(r => {
    if (r.rating && dist[r.rating] !== undefined) {
      dist[r.rating]++
    }
  })
  return dist
})

const averageRatingBySentiment = computed(() => {
  const sentiments = { positive: [], negative: [], neutral: [] }
  
  props.results.forEach(r => {
    if (r.rating && r.label) {
      const label = r.label.toLowerCase()
      if (label.includes('positive')) sentiments.positive.push(r.rating)
      else if (label.includes('negative')) sentiments.negative.push(r.rating)
      else if (label.includes('neutral')) sentiments.neutral.push(r.rating)
    }
  })
  
  return {
    positive: sentiments.positive.length > 0 
      ? sentiments.positive.reduce((a, b) => a + b, 0) / sentiments.positive.length 
      : 0,
    negative: sentiments.negative.length > 0 
      ? sentiments.negative.reduce((a, b) => a + b, 0) / sentiments.negative.length 
      : 0,
    neutral: sentiments.neutral.length > 0 
      ? sentiments.neutral.reduce((a, b) => a + b, 0) / sentiments.neutral.length 
      : 0
  }
})

// Вспомогательные функции
const getLanguageText = (language) => {
  const languages = {
    'ru': 'Русский',
    'en': 'English',
    'uk': 'Українська',
    'be': 'Беларуская',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'pl': 'Polski',
    'zh': '中文',
    'ja': '日本語',
    'ko': '한국어',
    'ar': 'العربية',
    'hi': 'हिन्दी'
  }
  return languages[language.toLowerCase()] || language.toUpperCase()
}

// Инициализация графиков
const initLanguageChart = () => {
  if (!languagePieRef.value || !hasLanguages.value) return
  
  languagePieChart = echarts.init(languagePieRef.value)
  
  const data = languageStats.value.map(stat => ({
    name: getLanguageText(stat.language),
    value: stat.count
  }))
  
  // Динамические цвета в зависимости от темы
  const textColor = isDark.value ? '#e0e0e0' : '#303133'
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '0%',
      left: 'center',
      textStyle: {
        color: textColor
      }
    },
    series: [{
      type: 'pie',
      radius: '60%',
      data,
      label: {
        color: textColor
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  
  languagePieChart.setOption(option)
}

const initRatingCharts = () => {
  if (!hasRatings.value) return
  
  // Динамические цвета в зависимости от темы
  const textColor = isDark.value ? '#e0e0e0' : '#303133'
  const axisLabelColor = isDark.value ? '#d0d0d0' : '#606266'
  const axisLineColor = isDark.value ? '#666' : '#dcdfe6'
  const splitLineColor = isDark.value ? '#444' : '#e4e7ed'
  
  // Гистограмма рейтингов
  if (ratingHistogramRef.value) {
    ratingHistogramChart = echarts.init(ratingHistogramRef.value)
    
    const dist = ratingDistribution.value
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      xAxis: {
        type: 'category',
        data: ['1⭐', '2⭐', '3⭐', '4⭐', '5⭐'],
        axisLabel: {
          color: axisLabelColor
        },
        axisLine: {
          lineStyle: {
            color: axisLineColor
          }
        }
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          color: axisLabelColor
        },
        axisLine: {
          lineStyle: {
            color: axisLineColor
          }
        },
        splitLine: {
          lineStyle: {
            color: splitLineColor
          }
        }
      },
      series: [{
        type: 'bar',
        data: [dist[1], dist[2], dist[3], dist[4], dist[5]],
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        label: {
          show: true,
          position: 'top',
          color: textColor
        }
      }]
    }
    
    ratingHistogramChart.setOption(option)
  }
  
  // Средний рейтинг по тональности
  if (ratingBySentimentRef.value) {
    ratingBySentimentChart = echarts.init(ratingBySentimentRef.value)
    
    const avgBySentiment = averageRatingBySentiment.value
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' }
      },
      xAxis: {
        type: 'category',
        data: ['Положительные', 'Нейтральные', 'Отрицательные'],
        axisLabel: {
          color: axisLabelColor
        },
        axisLine: {
          lineStyle: {
            color: axisLineColor
          }
        }
      },
      yAxis: {
        type: 'value',
        max: 5,
        min: 0,
        axisLabel: {
          color: axisLabelColor
        },
        axisLine: {
          lineStyle: {
            color: axisLineColor
          }
        },
        splitLine: {
          lineStyle: {
            color: splitLineColor
          }
        }
      },
      series: [{
        type: 'bar',
        data: [
          { value: avgBySentiment.positive.toFixed(2), itemStyle: { color: '#67c23a' } },
          { value: avgBySentiment.neutral.toFixed(2), itemStyle: { color: '#909399' } },
          { value: avgBySentiment.negative.toFixed(2), itemStyle: { color: '#f56c6c' } }
        ],
        label: {
          show: true,
          position: 'top',
          formatter: '{c}',
          color: textColor
        }
      }]
    }
    
    ratingBySentimentChart.setOption(option)
  }
}

const disposeCharts = () => {
  if (languagePieChart) {
    languagePieChart.dispose()
    languagePieChart = null
  }
  if (ratingHistogramChart) {
    ratingHistogramChart.dispose()
    ratingHistogramChart = null
  }
  if (ratingBySentimentChart) {
    ratingBySentimentChart.dispose()
    ratingBySentimentChart = null
  }
}

const handleResize = () => {
  languagePieChart?.resize()
  ratingHistogramChart?.resize()
  ratingBySentimentChart?.resize()
}

// Отслеживание изменений данных
watch(() => props.results, async () => {
  if (props.results.length > 0) {
    disposeCharts()
    await nextTick()
    initLanguageChart()
    initRatingCharts()
  }
}, { deep: true })

onMounted(() => {
  window.addEventListener('resize', handleResize)
  if (props.results.length > 0) {
    nextTick(() => {
      initLanguageChart()
      initRatingCharts()
    })
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  disposeCharts()
})
</script>

<style scoped>
.analytics-card {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.analytics-content {
  padding: 10px 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-row :deep(.el-statistic) {
  text-align: center;
  padding: 15px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  margin-bottom: 20px;
}

.language-stats,
.rating-stats {
  margin: 20px 0;
}

.language-stats h3,
.rating-stats h3 {
  margin-bottom: 20px;
  color: var(--el-text-color-primary);
  font-size: 18px;
}

.stats-row :deep(.el-statistic) {
  background: var(--el-fill-color-light);
  padding: 15px;
  border-radius: 8px;
}
</style>

