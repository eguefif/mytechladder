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
  <div class="signup">
    <div lass="signup">Sign up</div>
    <input name="username" v-model="email" placeholder="username">
    <input name="email" v-model="email" placeholder="email">
    <input name="password" v-model="password" placeholder="Password">
    <button @click="login">Login</button>
  </div>
</template>

.signup {
position: relative;
width: 100%;
height: 100%;
}

input {
width: 60%;
height: 10px;
background: #e0dede;
justify-content: center;
display: flex;
margin: 20px auto;
padding: 12px;
border: none;
outline: none;
border-radius: 5px;
}

button{
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
button:hover{
background: #6d44b8;
}

<style></style>
