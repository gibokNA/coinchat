/* eslint-disable prefer-const */
import { ref, inject } from 'vue'
import { defineStore } from 'pinia'
import { useMobileDetection } from 'vue3-mobile-detection'

export const use_global_store = defineStore('global_store', () => {
  const axios: any = inject('axios')  // inject axios

  const is_mobile = ref(false)

  let iter_count = 0

  renew_is_mobile()

  function renew_is_mobile() {
    iter_count += 1

    is_mobile.value = useMobileDetection().isMobile()

    if (iter_count <= 60) setTimeout(renew_is_mobile, 1000)
  }

  // 일단 6가지 공유 값을 true와 v1으로 설정.
  const is_chart_button_clicked = ref(true)
  const is_chatting_button_clicked = ref(true)
  const is_change_rate_per_time_button_clicked = ref(true)
  const is_rapid_change_button_clicked = ref(true)
  const is_live_trade_button_clicked = ref(true)
  const selected_checker_version = ref("v1")

  // 로컬저장소 참조후 값이 없으면 저장하고, 값이 있으면 불러오기.
  if (localStorage.getItem('is_chart_button_clicked') == null) localStorage.setItem('is_chart_button_clicked', JSON.stringify(is_chart_button_clicked.value))
  else is_chart_button_clicked.value = JSON.parse(localStorage.getItem('is_chart_button_clicked')!)
  if (localStorage.getItem('is_chatting_button_clicked') == null) localStorage.setItem('is_chatting_button_clicked', JSON.stringify(is_chatting_button_clicked.value))
  else is_chatting_button_clicked.value = JSON.parse(localStorage.getItem('is_chatting_button_clicked')!)
  if (localStorage.getItem('is_change_rate_per_time_button_clicked') == null) localStorage.setItem('is_change_rate_per_time_button_clicked', JSON.stringify(is_change_rate_per_time_button_clicked.value))
  else is_change_rate_per_time_button_clicked.value = JSON.parse(localStorage.getItem('is_change_rate_per_time_button_clicked')!)
  if (localStorage.getItem('is_rapid_change_button_clicked') == null) localStorage.setItem('is_rapid_change_button_clicked', JSON.stringify(is_rapid_change_button_clicked.value))
  else is_rapid_change_button_clicked.value = JSON.parse(localStorage.getItem('is_rapid_change_button_clicked')!)
  if (localStorage.getItem('is_live_trade_button_clicked') == null) localStorage.setItem('is_live_trade_button_clicked', JSON.stringify(is_live_trade_button_clicked.value))
  else is_live_trade_button_clicked.value = JSON.parse(localStorage.getItem('is_live_trade_button_clicked')!)
  if (localStorage.getItem('selected_checker_version') == null) localStorage.setItem('selected_checker_version', JSON.stringify(selected_checker_version.value))
  else selected_checker_version.value = JSON.parse(localStorage.getItem('selected_checker_version')!)

  const main_page_container_height = ref(1000)

  const ip_address = ref('')

  axios.get('https://ipv4.jsonip.com').then((response: { data: any }) => {
    let temp = response.data["ip"]

    if (temp.search(':') != -1) {
    temp = response.data["ip"].split(':')
    } else if (temp.search('.') != -1) {
    temp = response.data["ip"].split('.')
    }

    ip_address.value = '(' + temp[0] + '.' + temp[1] + ')'
  })

  const now_symbol = ref("BTCUSDT")

  function symbol_clicked(symbol: string) {
    now_symbol.value = symbol.replace("/","")
    localStorage.setItem("now_symbol", now_symbol.value)
  
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  function return_color(change_rate: number, side: string) {
    if (side === "long") {
      if (change_rate >= 3) {
        return 'background: rgb(34,193,195); background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(157,253,45,1) 100%);'
      } else if (change_rate >= 2) {
        return 'background-color: #86E57F;'
      } else {
        return 'background-color: #B7F0B1;'
      }
    } else {
      if (change_rate >= 3) {
        return 'background: rgb(230,34,34); background: linear-gradient(90deg, rgba(230,34,34,1) 0%, rgba(252,176,69,1) 100%);'
      } else if (change_rate >= 2) {
        return 'background-color: #F15F5F;'
      } else {
        return 'background-color: #FFA7A7;'
      }
    }
  }

  const is_mobile_left_bar_show = ref(false)

  return {
    is_chart_button_clicked,
    is_chatting_button_clicked,
    is_change_rate_per_time_button_clicked,
    is_rapid_change_button_clicked,
    is_live_trade_button_clicked,
    main_page_container_height,
    ip_address,
    selected_checker_version,
    now_symbol,
    symbol_clicked,
    return_color,
    is_mobile_left_bar_show,
    is_mobile
  }
})
