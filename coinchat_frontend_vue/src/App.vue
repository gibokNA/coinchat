<script setup lang="ts">
import { useMobileDetection } from 'vue3-mobile-detection'
import { onMounted, onBeforeUnmount, ref } from 'vue'

import Chatting_Input from './components/Chatting/Chatting_Input.vue'
import Left_Bar from './components/Left_Bar.vue'
import Chatting from './components/Chatting/Chatting.vue'
import Mobile_Header from './components/Mobile_Header.vue'

import { RouterView } from 'vue-router'
import { use_global_store } from '@/stores/global_store'
import { storeToRefs } from 'pinia'

const global_store = use_global_store()

const {
  is_chatting_button_clicked,
  is_mobile_left_bar_show,
  is_mobile
} = storeToRefs(global_store)

let is_start = ref(true)
let is_end = ref(false)

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

function up_button_clicked() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function down_button_clicked() {
  window.scrollTo({ top: 99999999999, behavior: 'smooth' })
}

function handleScroll(event: any) {
  

  if (event.target.scrollingElement.scrollTop == 0) {
    is_start.value = true
  } else {
    if (
      event.target.scrollingElement.scrollTop + 5 >=
      event.target.scrollingElement.scrollHeight - window.innerHeight
    ) {
      is_end.value = true
    } else {
      is_start.value = false
      is_end.value = false
    }
  }
}

function set_container_style(is_chatting_button_clicked: boolean) {
  if (is_mobile.value === true) {
    return 'position: absolute;width: auto;top: 0; left: 0; right: 0;outline: solid #2C333C 1px;background-color: #161A1E;color: white;'
  } else {
    let right: string
  
    if (is_chatting_button_clicked == true) right = "380px"
    else right = "0"
  
    return 'position: absolute;width: auto;top: 0;left: 200px;right: ' + right + ';min-height: 1200px;outline: solid #2C333C 1px;background-color: #161A1E;color: white;'
  }
}

</script>

<template>
  <BContainer fluid style="background-color: #161a1e; color: white;">
    
    <RouterView :style="set_container_style(is_chatting_button_clicked)"></RouterView>
    <Chatting v-if="is_chatting_button_clicked"></Chatting>
    <Chatting_Input v-if="is_chatting_button_clicked"></Chatting_Input>
    <Mobile_Header v-if="is_mobile == true"></Mobile_Header>
    <Left_Bar v-show="is_mobile == false || is_mobile_left_bar_show"></Left_Bar>

    <a
      v-if="is_mobile == true && is_start == false"
      @click="up_button_clicked"
      style="position: fixed; cursor: pointer; bottom: 120px; right: 35px; font-size: 50px; color: skyblue;"
      ><IBiArrowUpCircleFill/></a>
    <a
      v-if="is_mobile == true && is_end == false"
      @click="down_button_clicked"
      style="position: fixed; cursor: pointer; bottom: 50px; right: 35px; font-size: 50px; color: skyblue;"
      ><IBiChatRightDotsFill/></a>
  </BContainer>
</template>
