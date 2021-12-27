<template>
  <div class="text-center hero">
    <h5 class="mb-5">Enable your Telegram token here</h5>
    <div v-if="this.token">
      <p>You already have token</p>
      <p>{{this.token}}</p>
      <button id="remove" v-on:click="updateToken('')">Remove</button>
    </div>
    <div v-else>
      <p>
        You can receive it with <b>/get_token</b> command in bot
      </p>
      <div>
        <input v-model="enteredToken"/>
      </div>
      <button id="confirm" v-on:click="updateToken(enteredToken)">Confirm</button>
    </div>
  </div>
</template>

<script>
const CONFIG = require('../../config.json')
const API_URL = CONFIG['API_URL']

export default {
  name: "Token",
  methods: {
    updateToken(token) {
      if (!token){
        let warnResult = confirm("Are you sure to remove token?")
        if (!warnResult){
          return 0;
        }
      }
      fetch(API_URL + '/api/v1/users/data/' + this.userId, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-access-tokens': this.idToken,
        },
        body: JSON.stringify({
          "token": token,
        })
      })
      this.token = token
    }
  },
  data(){
    return {
      token: null,
      idToken: null,
      userId: null,
    }
  },
  mounted() {
    this.userId = this.$auth.user.email;
    this.idToken = Object.values(this.$auth.idToken)[0];
    fetch(API_URL + '/api/v1/users/data/' + this.userId, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': this.idToken,
      },
      })
      .then(response => response.json())
      .then(json => {
        this.token = json['token']
      })
  }
};
</script>

<style>

#confirm {
  padding: 12px 20px;
  margin: 8px 0;
  background-color: cornflowerblue;
  color: white;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

#confirm:hover {
  padding: 12px 20px;
  margin: 8px 0;
  background-color: rgba(100, 107, 237, 0.94);
  color: white;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

#confirm:active {
  padding: 12px 20px;
  margin: 8px 0;
  background-color: #646bed;
  color: white;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

#remove {
  padding: 12px 20px;
  margin: 8px 0;
  background-color: #b60e0e;
  color: white;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

#remove:hover {
  padding: 12px 20px;
  margin: 8px 0;
  background-color: rgba(182, 14, 14, 0.94);
  color: white;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

#remove:active {
  padding: 12px 20px;
  margin: 8px 0;
  background-color: rgba(166, 18, 18, 0.93);
  color: white;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
