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
    <h1>Sign up</h1>
    <input name="username" v-model="email" placeholder="username">
    <input name="email" v-model="email" placeholder="email">
    <input name="password" v-model="password" placeholder="Password">
    <button @click="login">Login</button>
  </div>
</template>

<style></style>
