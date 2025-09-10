<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1>页面未找到</h1>
      <p>抱歉，您访问的页面不存在或已被移除。</p>
      
      <div class="suggestions">
        <h3>您可以尝试：</h3>
        <ul>
          <li>检查网址是否正确</li>
          <li>返回首页重新导航</li>
          <li>使用搜索功能查找内容</li>
          <li>联系管理员获取帮助</li>
        </ul>
      </div>
      
      <div class="actions">
        <button @click="goHome" class="home-btn">返回首页</button>
        <button @click="goBack" class="back-btn">返回上页</button>
      </div>
    </div>
    
    <div class="illustration">
      <div class="illustration-content">
        <div class="planet"></div>
        <div class="astronaut">🚀</div>
        <div class="stars">
          <div class="star" v-for="i in 20" :key="i"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'NotFound',
  setup() {
    const router = useRouter()
    
    const goHome = () => {
      router.push('/')
    }
    
    const goBack = () => {
      router.go(-1)
    }
    
    return {
      goHome,
      goBack
    }
  }
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
  z-index: 2;
}

.error-code {
  font-size: 8rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  animation: float 3s ease-in-out infinite;
}

.not-found h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.not-found p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.suggestions {
  text-align: left;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 8px;
  backdrop-filter: blur(10px);
}

.suggestions h3 {
  margin-bottom: 1rem;
  color: #fff;
}

.suggestions ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestions li {
  padding: 0.5rem 0;
  position: relative;
  padding-left: 1.5rem;
}

.suggestions li:before {
  content: "→";
  position: absolute;
  left: 0;
  color: #ffd700;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.home-btn, .back-btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.home-btn {
  background: #ffd700;
  color: #333;
}

.home-btn:hover {
  background: #ffed4e;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.back-btn {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.back-btn:hover {
  background: white;
  color: #333;
  transform: translateY(-2px);
}

.illustration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
}

.illustration-content {
  position: relative;
  width: 100%;
  height: 100%;
}

.planet {
  position: absolute;
  top: 20%;
  right: 10%;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle at 30% 30%, #ff6b6b, #ee5a24);
  border-radius: 50%;
  opacity: 0.3;
  animation: rotate 20s linear infinite;
}

.astronaut {
  position: absolute;
  top: 60%;
  left: 15%;
  font-size: 3rem;
  animation: float 4s ease-in-out infinite;
  animation-delay: 1s;
}

.stars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.star {
  position: absolute;
  width: 2px;
  height: 2px;
  background: white;
  border-radius: 50%;
  animation: twinkle 2s ease-in-out infinite;
}

.star:nth-child(1) { top: 10%; left: 20%; animation-delay: 0s; }
.star:nth-child(2) { top: 20%; left: 80%; animation-delay: 0.5s; }
.star:nth-child(3) { top: 30%; left: 10%; animation-delay: 1s; }
.star:nth-child(4) { top: 40%; left: 90%; animation-delay: 1.5s; }
.star:nth-child(5) { top: 50%; left: 30%; animation-delay: 2s; }
.star:nth-child(6) { top: 60%; left: 70%; animation-delay: 0.3s; }
.star:nth-child(7) { top: 70%; left: 15%; animation-delay: 0.8s; }
.star:nth-child(8) { top: 80%; left: 85%; animation-delay: 1.3s; }
.star:nth-child(9) { top: 15%; left: 50%; animation-delay: 1.8s; }
.star:nth-child(10) { top: 25%; left: 60%; animation-delay: 0.2s; }
.star:nth-child(11) { top: 35%; left: 40%; animation-delay: 0.7s; }
.star:nth-child(12) { top: 45%; left: 25%; animation-delay: 1.2s; }
.star:nth-child(13) { top: 55%; left: 75%; animation-delay: 1.7s; }
.star:nth-child(14) { top: 65%; left: 55%; animation-delay: 0.4s; }
.star:nth-child(15) { top: 75%; left: 35%; animation-delay: 0.9s; }
.star:nth-child(16) { top: 85%; left: 65%; animation-delay: 1.4s; }
.star:nth-child(17) { top: 5%; left: 75%; animation-delay: 1.9s; }
.star:nth-child(18) { top: 95%; left: 45%; animation-delay: 0.1s; }
.star:nth-child(19) { top: 12%; left: 35%; animation-delay: 0.6s; }
.star:nth-child(20) { top: 88%; left: 25%; animation-delay: 1.1s; }

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@media (max-width: 768px) {
  .not-found {
    padding: 1rem;
  }
  
  .error-code {
    font-size: 6rem;
  }
  
  .not-found h1 {
    font-size: 2rem;
  }
  
  .not-found p {
    font-size: 1rem;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
  
  .home-btn, .back-btn {
    width: 200px;
  }
  
  .planet {
    width: 100px;
    height: 100px;
    top: 15%;
    right: 5%;
  }
  
  .astronaut {
    font-size: 2rem;
    top: 70%;
    left: 10%;
  }
}
</style>