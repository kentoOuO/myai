import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // 监听所有的网络接口，包括 IPv4 地址
    port: 3000,      // 你可以指定端口
  },
})
