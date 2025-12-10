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
  GridComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'Количество по категориям'
  }
})

// Получаем информацию о текущей теме
const isDark = inject('isDark', ref(false))

const chartOption = computed(() => {
  const stats = {}
  props.data.forEach(item => {
    const label = item.label || 'unknown'
    stats[label] = (stats[label] || 0) + 1
  })

  const categories = Object.keys(stats).map(getLabelText)
  const values = Object.values(stats)
  const colors = Object.keys(stats).map(getLabelColor)

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
      axisPointer: {
        type: 'shadow'
      }
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
      axisLabel: {
        interval: 0,
        rotate: 30,
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
      name: 'Количество',
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
        data: values.map((value, index) => ({
          value: value,
          itemStyle: {
            color: colors[index]
          }
        })),
        barWidth: '60%',
        label: {
          show: true,
          position: 'top',
          color: textColor
        },
        emphasis: {
          focus: 'series'
        }
      }
    ]
  }
})

const getLabelText = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive')) return 'Положительная'
  if (labelLower.includes('negative')) return 'Отрицательная'
  if (labelLower.includes('neutral')) return 'Нейтральная'
  return label
}

const getLabelColor = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive')) return '#67c23a'
  if (labelLower.includes('negative')) return '#f56c6c'
  if (labelLower.includes('neutral')) return '#909399'
  return '#409EFF'
}
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

