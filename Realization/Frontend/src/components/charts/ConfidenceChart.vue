<template>
  <div class="chart-container">
    <v-chart 
      :option="chartOption" 
      :autoresize="true"
      style="height: 450px;"
    />
  </div>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  MarkLineComponent,
  MarkAreaComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  MarkLineComponent,
  MarkAreaComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'График уверенности модели'
  }
})

// Получаем информацию о текущей теме
const isDark = inject('isDark', ref(false))

const chartOption = computed(() => {
  const confidenceData = props.data.map((item, index) => {
    // Получаем уверенность из разных источников
    let confidence = 0
    if (item.confidence !== undefined) {
      confidence = item.confidence
    } else if (item.probs && Array.isArray(item.probs) && item.probs.length > 0) {
      confidence = Math.max(...item.probs)
    }
    return {
      index: index + 1,
      confidence: (confidence * 100).toFixed(2),
      label: item.label
    }
  })

  // Динамические цвета в зависимости от темы
  const textColor = isDark.value ? '#e0e0e0' : '#303133'
  const axisLabelColor = isDark.value ? '#d0d0d0' : '#606266'
  const axisLineColor = isDark.value ? '#666' : '#dcdfe6'
  const splitLineColor = isDark.value ? '#444' : '#e4e7ed'

  return {
    title: {
      text: props.title,
      left: 'center',
      top: 10,
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: textColor
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const data = params[0]
        return `Текст #${data.name}<br/>Уверенность: ${data.value}%`
      }
    },
    grid: {
      left: '8%',
      right: '8%',
      top: '15%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: confidenceData.map(d => d.index),
      name: 'Номер текста',
      nameTextStyle: {
        color: axisLabelColor,
        fontSize: 12
      },
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
      name: 'Уверенность (%)',
      min: 0,
      max: 100,
      nameTextStyle: {
        color: axisLabelColor,
        fontSize: 12
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
    dataZoom: [
      {
        type: 'slider',
        start: 0,
        end: 100,
        textStyle: {
          color: axisLabelColor
        }
      }
    ],
    visualMap: {
      show: false,
      dimension: 1,
      pieces: [
        { lte: 50, color: '#f56c6c' },
        { gt: 50, lte: 75, color: '#e6a23c' },
        { gt: 75, color: '#67c23a' }
      ]
    },
    series: [
      {
        name: 'Уверенность',
        type: 'line',
        data: confidenceData.map(d => d.confidence),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 2
        },
        areaStyle: {
          opacity: 0.3
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderWidth: 3
          }
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

