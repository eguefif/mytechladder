<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { postAccount } from '@/services/index'
import type { Account } from '@/services/types'

const email: Ref<string, string> = ref("")
const password: Ref<string, string> = ref("")
const username: Ref<string, string> = ref("")

async function login() {
  let account: Account = {
    email: email.value,
    username: username.value,
    password: password.value
  }
  try {
    let response = await postAccount(account);
    console.log(response)
  } catch (e) {
    console.log(`error: ${e}`)
  }
}

</script>

<template>
  <div class="signup">
    <span class="signupTitle">Sign up</span>
    <input name="username" v-model="username" placeholder="username">
    <input name="email" v-model="email" placeholder="email">
    <input name="password" v-model="password" placeholder="Password">
    <button @click="login">Login</button>
  </div>
</template>

<style scoped>
.signup {
  position: relative;
  width: 100%;
  height: 100%;
}

.signupTitle {
  display: block;
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #573b8a;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
}

input {
  width: 60%;
  height: 10px;
  background: #e0dede;
  justify-content: center;
  display: flex;
  margin: 10px auto;
  padding: 12px;
  border: none;
  outline: none;
  border-radius: 5px;
}

button {
  width: 60%;
  height: 40px;
  margin: 10px auto;
  justify-content: center;
  display: block;
  color: #fff;
  background: #573b8a;
  font-size: 1em;
  font-weight: bold;
  margin-top: 30px;
  outline: none;
  border: none;
  border-radius: 5px;
  transition: .2s ease-in;
  cursor: pointer;
}

button:hover {
  background: #6d44b8;
}
</style>
