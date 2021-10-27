<template>
  <div id="app">
    <img alt="Financial assistant logo" src="./assets/logo.png" height="200">
    <br>
    <h2>Welocme to bot admin {{this.user_name}}!</h2>
    <input v-model="token" v-on:change="tokenEvent(token)" placeholder="put your token here, please">
    <br>
    <div v-if="this.user_name">
      <Cryptos
        v-bind:user_cryptos="this.user_assets['user_cryptos']"
        v-on:add-crypto="addAsset"
        v-on:remove-crypto="deleteAsset"
      />
      <Stocks
        v-bind:user_stocks="this.user_assets['user_stocks']"
        v-on:add-stock="addAsset"
        v-on:remove-stock="deleteAsset"
      />
      <Currencies
        v-bind:user_currencies="this.user_assets['user_currencies']"
        v-on:add-currencies="addAsset"
        v-on:remove-currencies="deleteAsset"
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

let CONFIG = require('./config.json')
let API_URL = CONFIG['API_URL']

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
    addAsset(asset, typeId){
      for (let type_id in this.user_assets){
        if (!this.user_assets[type_id].includes(asset) && (type_id === typeId)){
          this.user_assets[type_id].push(asset)
          this.updateData(this.user_id)
        }
      }
    },
    deleteAsset(asset, typeId){
      this.user_assets[typeId] = this.user_assets[typeId].filter(item => item !== asset)
      this.updateData(this.user_id)
    },
    getData(user_id){
      fetch(API_URL + `/api/v1/users/` + user_id)
      .then(response => response.json())
      .then(json => {
        this.user_name = json['user_name']
        this.user_assets = json['user_assets']
      })
    },
    updateData(user_id){
      fetch(API_URL + `/api/v1/users/` + user_id, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "user_assets": this.user_assets,
        })
      })
    }
  },
  data(){
      return {
          user_id: null,
          user_name: null,
          user_assets: {},
      }
  },
  mounted(){
      fetch(API_URL + '/api/v1/users/' + this.user_id)
        .then(response => response.json())
        .then(json => {
            this.user_name = json['user_name']
            this.user_assets = json['user_assets']
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
