<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'

const email: Ref<string, string> = ref("")
const password: Ref<string, string> = ref("")

function login() {
  console.log(`${email.value} - ${password.value}`)
}

</script>

<template>
  <div>
    <input name="username" v-model="email" placeholder="Email">
    <input name="password" v-model="password" placeholder="Password">
    <button @click="login">Login</button>
  </div>
</template>

<style></style>
