<template>
  <div class="container">
    <div class="row align-items-center profile-header">
      <div class="col-md-2 mb-3">
        <img
          :src="$auth.user.picture"
          alt="User's profile picture"
          class="rounded-circle img-fluid profile-picture"
        />
      </div>
      <div class="col-md text-center text-md-left">
        <h2>{{ $auth.user.name }}</h2>
        <p class="lead text-muted">{{ $auth.user.email }}</p>
      </div>
    </div>

    <div id="assetTables">
      <div>
        <Cryptos
            v-bind:user_cryptos="this.userAssets['user_cryptos']"
            v-on:add-crypto="addAsset"
            v-on:remove-crypto="deleteAsset"
        />
        <Stocks
            v-bind:user_stocks="this.userAssets['user_stocks']"
            v-on:add-stock="addAsset"
            v-on:remove-stock="deleteAsset"
        />
        <Currencies
            v-bind:user_currencies="this.userAssets['user_currencies']"
            v-on:add-currencies="addAsset"
            v-on:remove-currencies="deleteAsset"
        />
      </div>
    </div>
  </div>
</template>


<script>
import Cryptos from '../components/Cryptos.vue'
import Currencies from "../components/Currencies";
import Stocks from "../components/Stocks";

const CONFIG = require('../../config.json')
const API_URL = CONFIG['API_URL']

export default {
  name: 'Profile',
  components: {
    Stocks,
    Currencies,
    Cryptos
  },
  methods: {
    addAsset(asset, typeId){
      if (!asset){
        return
      }
      fetch(API_URL + `/api/v1/assets`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-access-tokens': this.idToken,
        },
        body: JSON.stringify({
          "user_id": this.userId,
          "ticker": asset,
          "type_id": typeId
        })
      })
      // FIXME
      if (!this.userAssets[typeId].includes(asset)){
        this.userAssets[typeId].push(asset)
      }
    },
    deleteAsset(asset, typeId){
      fetch(API_URL + `/api/v1/assets/` + typeId + '/' + asset, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'x-access-tokens': this.idToken,
        }
      })
      // FIXME
      this.userAssets[typeId] = this.userAssets[typeId].filter(item => item !== asset)
    },
    getData(){
      fetch(API_URL + `/api/v1/users/` + this.userId,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'x-access-tokens': this.idToken,
        },
      })
      .then(response => response.json())
      .then(json => {
        this.userAssets = json['user_assets']
      })
    }
  },
  data(){
    return {
      userId: null,
      userAssets: {},
    }
  },
  mounted(){
    this.userId = this.$auth.user.email;
    this.idToken = Object.values(this.$auth.idToken)[0];

    fetch(API_URL + '/api/v1/users/' + this.userId, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'x-access-tokens': this.idToken,
      },
    })
    .then(response => response.json())
    .then(json => {
      this.userAssets = json['user_assets']
    })
  }
}
</script>


<style>
#assetTables {
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
