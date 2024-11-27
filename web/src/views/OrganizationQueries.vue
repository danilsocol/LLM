<template>
  <div class="history-container">
    <h1>История организации</h1>
    <button @click="goBack" class="back-button">Назад</button>

    <!-- Секция запросов -->
    <h2>История запросов</h2>
    <table>
      <thead>
      <tr>
        <th>ID</th>
        <th>Пользователь (ID)</th>
        <th>Вопрос</th>
        <th>Ответ</th>
        <th>Документ (ID)</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="query in queries" :key="query.id">
        <td>{{ query.id }}</td>
        <td>{{ query.user_id }}</td>
        <td>{{ query.question }}</td>
        <td v-if="query.answer">{{ query.answer }}</td>
        <td v-else>Ожидает ответа</td>
        <td>{{ query.document_id || '-' }}</td>
      </tr>
      </tbody>
    </table>

    <!-- Секция транзакций -->
    <h2>История транзакций</h2>
    <table>
      <thead>
      <tr>
        <th>ID</th>
        <th>Пользователь (ID)</th>
        <th>Тип</th>
        <th>Сумма</th>
        <th>Дата</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="transaction in transactions" :key="transaction.id">
        <td>{{ transaction.id }}</td>
        <td>{{ transaction.user_id }}</td>
        <td>
          <span :class="{'transaction-type': true,
                        'spend': transaction.type === 'spend',
                        'deposit': transaction.type === 'deposit'}">
            {{ transaction.type === 'spend' ? 'Списание' : 'Пополнение' }}
          </span>
        </td>
        <td>{{ transaction.amount }}</td>
        <td>{{ formatDate(transaction.created_at) }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import { getQueriesByOrganizationId, getTransactionsByOrganizationId } from "@/services/api";

export default {
  data() {
    return {
      queries: [],
      transactions: []
    };
  },
  async mounted() {
    const organizationId = this.$route.params.organizationId;
    try {
      // Загружаем запросы и транзакции параллельно
      const [queriesData, transactionsData] = await Promise.all([
        getQueriesByOrganizationId(organizationId),
        getTransactionsByOrganizationId(organizationId)
      ]);

      this.queries = queriesData;
      this.transactions = transactionsData;
    } catch (error) {
      console.error("Ошибка при получении данных:", error);
      alert("Не удалось загрузить данные.");
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString();
    }
  }
};
</script>

<style scoped>
.history-container {
  padding: 20px;
  background-color: #f4f4f4;
  min-height: 100vh;
}

h2 {
  margin-top: 30px;
  color: #333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  margin-bottom: 30px;
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
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #0056b3;
}

.transaction-type {
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.spend {
  background-color: #ffebee;
  color: #d32f2f;
}

.deposit {
  background-color: #e8f5e9;
  color: #2e7d32;
}
</style>