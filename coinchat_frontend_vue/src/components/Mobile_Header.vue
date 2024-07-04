<script setup lang="ts">
import { useRouter } from 'vue-router'
import { use_global_store } from '@/stores/global_store'
import { storeToRefs } from 'pinia'

const router = useRouter()

const global_store = use_global_store()

const {
  is_mobile_left_bar_show
} = storeToRefs(global_store)

function nav_button_clicked() {
    window.scrollTo({top: 0, behavior: 'smooth'});

    setTimeout(() => {
        router.go(0)
    }, 300);
}

</script>

<template>
    <BContainer fluid="true" style="height: 60px;top: 0;left: 0;right: 0;position: fixed;outline: solid #2C333C 1px;background-color: #20262C;">
        <BRow align-h="between" align-v="center">
            <BCol cols="auto" @click="nav_button_clicked" style="margin-top: 5px;">
                <BImg src="https://coinchat.work/1.png" fluid="true" style="max-height: 50px;"></BImg>
                <span style="font-size: large;"> 코인챗</span>
            </BCol>
            <BCol cols="auto" style="margin-right: 30px;">
                <IBiList style="color: white; font-size: 40px; margin-top: 5px;" v-if="is_mobile_left_bar_show==false" @click="() => is_mobile_left_bar_show = !is_mobile_left_bar_show" />
                <IBiChevronDoubleLeft style="color: white; font-size: 40px; margin-top: 5px;" v-if="is_mobile_left_bar_show==true" @click="() => is_mobile_left_bar_show = !is_mobile_left_bar_show" />
            </BCol>
        </BRow>
    </BContainer>
</template>