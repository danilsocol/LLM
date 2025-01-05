<template>
  <div class="queries-container">
    <h1>Мои запросы</h1>
    <button @click="goBack" class="back-button">Назад</button>
    <table>
      <thead>
      <tr>
        <th>ID</th>
        <th>Вопрос</th>
        <th>Ответ</th>
        <th>Документ (ID)</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="query in queries" :key="query.id">
        <td>{{ query.id }}</td>
        <td>{{ query.question }}</td>
        <td v-if="query.answer">{{ query.answer }}</td>
        <td v-else>Ожидает ответа</td>
        <td>{{ query.document_id || '-' }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {getCurrentUser, getQueriesByUserId} from "@/services/api";


export default {
  data() {
    return {
      queries: []
    };
  },
  async mounted() {
    const user = await getCurrentUser();
    try {
      this.queries = await getQueriesByUserId(user.id);
    } catch (error) {
      console.error("Ошибка при получении запросов:", error);
      alert("Не удалось загрузить список запросов.");
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },

  }
};
</script>

<style scoped>
.queries-container {
  padding: 20px;
  background-color: #f4f4f4;
  min-height: 100vh;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #007bff;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}


.back-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px; /* Added margin */
}

.back-button:hover {
  background-color: #0056b3;
}



</style>