<template>
  <div class="chart-container">
    <v-chart 
      :option="chartOption" 
      :autoresize="true"
      style="height: 350px;"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { GaugeChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  GaugeChart,
  TitleComponent,
  TooltipComponent
])

const props = defineProps({
  value: {
    type: Number,
    required: true,
    default: 0
  },
  title: {
    type: String,
    default: 'Средняя уверенность модели'
  }
})

const chartOption = computed(() => {
  const percentage = (props.value * 100).toFixed(1)
  
  return {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    series: [
      {
        type: 'gauge',
        startAngle: 180,
        endAngle: 0,
        min: 0,
        max: 100,
        splitNumber: 10,
        axisLine: {
          lineStyle: {
            width: 6,
            color: [
              [0.5, '#f56c6c'],
              [0.75, '#e6a23c'],
              [1, '#67c23a']
            ]
          }
        },
        pointer: {
          icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
          length: '12%',
          width: 20,
          offsetCenter: [0, '-60%'],
          itemStyle: {
            color: 'auto'
          }
        },
        axisTick: {
          length: 12,
          lineStyle: {
            color: 'auto',
            width: 2
          }
        },
        splitLine: {
          length: 20,
          lineStyle: {
            color: 'auto',
            width: 5
          }
        },
        axisLabel: {
          color: '#464646',
          fontSize: 12,
          distance: -60,
          formatter: function (value) {
            if (value === 50) return 'Средне'
            if (value === 75) return 'Хорошо'
            if (value === 100) return 'Отлично'
            return ''
          }
        },
        title: {
          offsetCenter: [0, '-20%'],
          fontSize: 14
        },
        detail: {
          fontSize: 30,
          offsetCenter: [0, '0%'],
          valueAnimation: true,
          formatter: function (value) {
            return value.toFixed(1) + '%'
          },
          color: 'auto'
        },
        data: [
          {
            value: percentage,
            name: 'Уверенность'
          }
        ]
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

