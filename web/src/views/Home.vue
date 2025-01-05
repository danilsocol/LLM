<template>
  <div class="home-container">
    <div class="content">
      <h1>Добро пожаловать на DockForYou!</h1>
      <p>
        DockForYou - это платформа для быстрого поиска ответов внутри организационной документации. Вы можете загрузить свои документы и позволить сотрудникам/коллегам быстро анализировать информацию на основе их запросов.
      </p>

      <h2>Как это работает?</h2>
      <p>
        Данные из ваших документов загружаются вместе с вашим запросом в нейронную сеть. Нейросеть анализирует информацию и предоставляет точный ответ на ваш вопрос, помогая вам быстро находить и актуализировать нужные сведения.
      </p>

      <h2>Основные функции:</h2>
      <ul>
        <li><strong>Управление организацией:</strong> Создавайте и настраивайте профили организаций.</li>
        <li><strong>Управление пользователями:</strong> Добавляйте и управляйте пользователями вашей организации.</li>
        <li><strong>Управление документацией:</strong> Загружайте, храните и организовывайте ваши документы.</li>
        <li><strong>Помощь в поиске:</strong> Быстрый и точный поиск информации в ваших документах.</li>
        <li><strong>Актуализация информации:</strong> Поддерживайте актуальность данных для всех сотрудников.</li>
      </ul>

      <div v-if="!isLoggedIn" class="login-section">
        <router-link to="/login">Войти в аккаунт</router-link>
      </div>
      <div v-else class="user-section">
        <button @click="logout">Выйти</button>
        <router-link to="/user">Мой профиль</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import {removeToken} from '../services/auth';
import {getCurrentUser} from "@/services/api.js";

export default {
  data() {
    return {
      user: null
    };
  },
  computed: {
    isLoggedIn() {
      return this.user !== null;
    },
  },
  async mounted() {
    this.user = await getCurrentUser();
  },
  methods: {
    logout() {
      this.user = null
      removeToken();
    }
  }
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f4;
}

.content {
  width: 80%;
  max-width: 800px;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: left;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

p {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

h2 {
  color: #333;
  margin-top: 30px;
  margin-bottom: 15px;
}

ul {
  list-style: disc;
  margin-left: 20px;
  margin-bottom: 20px;
}

li {
  color: #666;
  margin-bottom: 10px;
}

.login-section, .user-section {
  margin-top: 30px;
  text-align: center;
}

a {
  color: #007bff;
  text-decoration: none;
  margin: 0 10px;
  padding: 10px 15px;
  border: 1px solid #007bff;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

a:hover {
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
}

button {
  color: #fff;
  background-color: #dc3545; /* Красный цвет для кнопки выхода */
  border: none;
  border-radius: 4px;
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  margin-left: 10px; /* Отступ слева для кнопки выхода */
}
</style>