<template>
  <div class="register-container">
    <div class="register-form">
      <h2>Регистрация</h2>
      <form @submit.prevent="register">
        <div class="input-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="input-group">
          <label for="password">Пароль:</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <button type="submit" :disabled="loading">
          <span v-if="loading">Регистрация...</span>
          <span v-else>Зарегистрироваться</span>
        </button>
      </form>
      <p>Уже есть аккаунт? <router-link to="/login">Войдите</router-link></p>
    </div>
  </div>
</template>

<script>
import { register } from '../services/api';
import { setUser } from '../services/auth';
import {User} from "@/models/models.js";

export default {
  data() {
    return {
      email: '',
      password: '',
      error: null,
      loading: false
    };
  },
  methods: {
    async register() {
      this.error = null;
      this.loading = true;
      try {
        const response = await register(this.email, this.password);
        const user = new User(
            response.id,
            response.role,
            response.email,
            response.password,
            response.organizationId || null
        );
        setUser(user);
        this.$router.push('/');
      } catch (error) {
        console.error("Ошибка регистрации:", error);
        this.loading = false;
        if (error.response) {
          if (error.response.status === 400 && error.response.data.detail) {
            this.error = error.response.data.detail.join('\n');
          } else {
            this.error = "Ошибка при регистрации. Попробуйте позже.";
          }
        } else {
          this.error = "Произошла ошибка при регистрации. Попробуйте позже.";
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f4;
}

.register-form {
  background-color: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.input-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-bottom: 10px;
}

p {
  text-align: center;
  margin-top: 20px;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>