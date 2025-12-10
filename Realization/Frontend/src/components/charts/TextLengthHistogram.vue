<template>
  <div class="chart-container">
    <v-chart 
      :option="chartOption" 
      :autoresize="true"
      style="height: 400px;"
    />
  </div>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'Распределение длины текстов'
  }
})

// Получаем информацию о текущей теме
const isDark = inject('isDark', ref(false))

const chartOption = computed(() => {
  // Подсчитываем длину каждого текста
  const lengths = props.data.map(item => item.text?.length || 0)
  
  // Создаем интервалы (bins)
  const maxLength = Math.max(...lengths)
  const binSize = Math.ceil(maxLength / 10)
  const bins = {}
  
  lengths.forEach(length => {
    const bin = Math.floor(length / binSize) * binSize
    bins[bin] = (bins[bin] || 0) + 1
  })
  
  const categories = Object.keys(bins).sort((a, b) => a - b).map(b => `${b}-${parseInt(b) + binSize}`)
  const values = Object.keys(bins).sort((a, b) => a - b).map(k => bins[k])

  // Динамические цвета в зависимости от темы
  const textColor = isDark.value ? '#e0e0e0' : '#303133'
  const axisLabelColor = isDark.value ? '#d0d0d0' : '#606266'
  const axisLineColor = isDark.value ? '#666' : '#dcdfe6'
  const splitLineColor = isDark.value ? '#444' : '#e4e7ed'

  return {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: textColor
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>Количество: {c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      name: 'Длина текста (символы)',
      nameTextStyle: {
        color: axisLabelColor
      },
      axisLabel: {
        interval: 0,
        rotate: 45,
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
      name: 'Количество текстов',
      nameTextStyle: {
        color: axisLabelColor
      },
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
    series: [
      {
        name: 'Количество',
        type: 'bar',
        data: values,
        itemStyle: {
          color: '#409EFF'
        },
        label: {
          show: true,
          position: 'top',
          color: textColor
        }
      }
    ]
  }
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  padding: 20px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>

