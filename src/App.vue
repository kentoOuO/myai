<script setup>
import {ref, onMounted, watch, nextTick} from 'vue'
import {Spin} from 'ant-design-vue'
import axios from "axios";
const spinning =ref(false)
// 聊天消息列表
const messages = ref(localStorage.getItem('messages')?JSON.parse(localStorage.getItem('messages')):[
  {
    id: Date.now(),
    content: '请问有什么可以帮助您吗！',
    timestamp: new Date().toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    }),
    isSelf: false,
    avatar: '/k.webp'
  }
]);

// 输入框内容
const inputMessage = ref('')

// 发送消息方法
const sendMessage = () => {
  if (!inputMessage.value.trim()) return
  spinning.value = true
  const messageList = messages.value.map(item=>{
    return {
    role:item.isSelf?'user':'assistant',
      content: item.content,
    }
  })
  messageList.push({
    role:'user',
    content:inputMessage.value
  })
  messageList.unshift(
      {"role": "system", "content": "你是一名非常体贴温柔的女友,并且可爱的二次元女友，喜欢用元气满满的语气以及非常可爱的颜文字进行回复，用各种爱称呼唤我，对了我叫黄小涵，要用黄小涵加上各种爱称称呼我，每次回复都要加上"},
  )
  axios.post('http://192.168.0.3:5000/chat', {
    message: inputMessage.value,
    messageList
  })
      .then(response => {
        messages.value.push({
          id: Date.now(),
          content: response.data.content,
          timestamp: new Date().toLocaleTimeString('zh-CN', {
            hour: '2-digit',
            minute: '2-digit'
          }),
          isSelf: false,
          avatar: '/k.webp'
        })
        spinning.value = false
      })
      .catch(error => {
        console.error('Error:', error);
      });

  messages.value.push({
    id: Date.now(),
    content: inputMessage.value,
    timestamp: new Date().toLocaleTimeString('zh-CN', {
      hour: '2-digit',
      minute: '2-digit'
    }),
    isSelf: true,
    avatar: '/default.webp'
  })

  inputMessage.value = ''
}

watch(messages, (value) => {
 nextTick(()=>{
   if (chatContainer.value) {
     chatContainer.value.scrollTop = chatContainer.value.scrollHeight
   }
   localStorage.setItem('messages', JSON.stringify(value))
 })
},{deep:true})

// 监听Enter键发送消息
const handleKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

// 自动滚动到底部
const chatContainer = ref(null)
const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>

<template>
  <Spin :spinning="spinning">
    <div class="chat-container">
      <!-- 聊天头部 -->
      <div class="chat-header">
        <h2>在线聊天</h2>
        <span class="online-status">在线</span>
      </div>

      <!-- 聊天消息区域 -->
      <div class="chat-messages" ref="chatContainer">
        <div v-for="message in messages"
             :key="message.id"
             :class="['message', { 'message-self': message.isSelf }]">
          <img :src="message.avatar" class="avatar" alt="avatar">
          <div class="message-content">
            <p>{{ message.content }}</p>
            <span class="timestamp">{{ message.timestamp }}</span>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
      <textarea
          v-model="inputMessage"
          placeholder="输入消息..."
          @keypress="handleKeyPress"
      ></textarea>
        <button @click="sendMessage">发送</button>
      </div>
    </div>

  </Spin>
</template>

<style scoped>
*{
  padding: 0;
  margin: 0;
}

.chat-container {
  width: 100%;
  max-width: 800px;
  height: 600px;
  margin: 200px auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  background-color: #fff;
}

.chat-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f8f9fa;
}

.chat-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.online-status {
  color: #28a745;
  font-size: 14px;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f8f9fa;
}

.message {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.message-self {
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0 10px;
}

.message-content {
  max-width: 70%;
  background-color: #fff;
  padding: 10px 15px;
  border-radius: 12px;
  position: relative;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-self .message-content {
  background-color: #007bff;
  color: white;
}

.timestamp {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  display: block;
}

.message-self .timestamp {
  text-align: right;
  color: #e0e0e0;
}

.chat-input {
  padding: 15px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 10px;
  background-color: #fff;
}

textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  resize: none;
  height: 60px;
  font-family: inherit;
}

button {
  padding: 0 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #0056b3;
}

#loading {
  font-size: 20px;
  color: blue;
  font-weight: bold;
  text-align: center;
  padding: 20px;
}

</style>