<template>
  <div id="app">
    <img alt="Financial assistant logo" src="./assets/logo.png" height="200">
    <br>
    <h2>Welocme to bot admin {{this.user_name}}!</h2>
    <input v-model="token" v-on:change="tokenEvent(token)" placeholder="put your token here, please">
    <br>
    <div v-if="this.user_name">
      <Cryptos
        v-bind:user_cryptos="user_cryptos"
        v-on:add-crypto="addCrypto"
        v-on:remove-crypto="deleteCrypto"
      /> 
      <Stocks
        v-bind:user_stocks="user_stocks"
        v-on:add-stock="addStock"
        v-on:remove-stock="deleteStock"
      />
      <Currencies
        v-bind:user_currencies="user_currencies"
        v-on:add-currencies="addCurrencie"
        v-on:remove-currencies="deleteCurrencie"
      />
    </div>
    <div v-else-if="this.user_name===null">
    </div>
    <div v-else>
      <br>
      <h3>Please enter correct token!</h3>
    </div>
  </div>
</template>

<script>
import Stocks from './components/Stocks.vue'
import Currencies from './components/Currencies.vue'
import Cryptos from './components/Cryptos.vue'

// this is link to API url (now local)
let API_URL = 'http://127.0.0.1:5000'

export default {
  name: 'App',
  components: {
    Stocks,
    Currencies,
    Cryptos
  },
  methods: {
    tokenEvent: function (token) {
      this.user_id = token
      this.getData(token)
    },
    addStock(i){
      if (!this.user_stocks.includes(i)){
        this.user_stocks.push(i)
        this.updateData(this.user_id)
      }
    },
    deleteStock(i){
      this.user_stocks = this.user_stocks.filter(item => item !== i)
      this.updateData(this.user_id)
    },
    addCurrencie(i){
      if (!this.user_currencies.includes(i)){
        this.user_currencies.push(i)
        this.updateData(this.user_id)
      }
    },
    deleteCurrencie(i){
      this.user_currencies = this.user_currencies.filter(item => item !== i)
      this.updateData(this.user_id)
    },
    addCrypto(i){
      if (!this.user_cryptos.includes(i)){
        this.user_cryptos.push(i)
        this.updateData(this.user_id)
      }
    },
    deleteCrypto(i){
      this.user_cryptos = this.user_cryptos.filter(item => item !== i)
      this.updateData(this.user_id)
    },
    getData(token){
      fetch(API_URL + `/api/v1/users/` + token)
      .then(response => response.json())
      .then(json => {
        this.user_name = json['user_name']
        this.user_stocks = json['user_assets']['user_stocks']
        this.user_currencies = json['user_assets']['user_currencies']
        this.user_cryptos = json['user_assets']['user_cryptos']
        this.user_resources = json['user_assets']['user_resources']
      })
    },
    updateData(i){
      fetch(API_URL + `/api/v1/users/` + i, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "user_assets": {
            "user_stocks": this.user_stocks,
            "user_currencies": this.user_currencies,
            "user_cryptos": this.user_cryptos,
            "user_resources": this.user_resources,
          }
        })
      })
    }
  },
  data(){
      return {
          user_id: null,
          user_name: null,
          user_stocks: [],
          user_currencies: [],
          user_cryptos: [],
          user_resources: [],
      }
  },
  mounted(){
      fetch(API_URL + '/api/v1/users/' + this.user_id)
        .then(response => response.json())
        .then(json => {
            this.user_name = json['user_name']
            this.user_stocks = json['user_assets']['user_stocks']
            this.user_currencies = json['user_assets']['user_currencies']
            this.user_cryptos = json['user_assets']['user_cryptos']
            this.user_resources = json['user_assets']['user_resources']
        })
  }
}
</script>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  input {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
</style>
