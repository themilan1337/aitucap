<script setup lang="ts">
import { Icon } from '@iconify/vue'

defineProps<{
  currentStep: number
  totalSteps: number
}>()

const emit = defineEmits<{
  back: []
}>()

const goBack = () => emit('back')
</script>

<template>
  <div class="w-full mb-8">
    <div class="flex gap-1 mb-6">
      <div 
        v-for="step in totalSteps" 
        :key="step"
        class="h-1 flex-1 rounded-full transition-all duration-300"
        :class="step <= currentStep ? 'bg-[#CCFF00]' : 'bg-[#2A2A2A]'"
      />
    </div>
    
    <div class="flex items-center justify-between">
      <button 
        class="w-10 h-10 rounded-full bg-[#1A1A1A] flex items-center justify-center text-white active:scale-90 transition-transform cursor-pointer"
        @click="goBack"
      >
        <Icon icon="hugeicons:arrow-left-02" class="text-xl" />
      </button>
      
      <span class="text-gray-500 font-medium">{{ currentStep }}/{{ totalSteps }}</span>
    </div>
  </div>
</template>
