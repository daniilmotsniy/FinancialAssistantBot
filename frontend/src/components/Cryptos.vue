<template>
    <div>
        <h3>Here we have list of your cryptos</h3>
        <br>
        <table id="data">
            <tr>
                <th>Crypto</th>
                <th>Ticker</th>
                <th>Delete</th>
            </tr>
            <tr v-for="crypto in user_cryptos" :key="crypto">
                <td>{{ cryptoDict[crypto] }}</td>
                <td>{{ crypto }}</td>
                <td><a id="delete" v-on:click="$emit('remove-crypto', crypto, 'user_cryptos')">Delete</a></td>
            </tr>
        </table>
        <br>
        <div class="grid">
          <Autocomplete
              :search="search"
              placeholder="Search for a crypto"
              aria-label="Search for a crypto"
              @submit="onSubmit"
          ></Autocomplete>
        </div>
        <br>
    </div>
</template>

<script>
  import Autocomplete from "@trevoreyre/autocomplete-vue"

  export default ({
      props: ['user_cryptos'],
      components: {
        Autocomplete
      },
      methods: {
        search(input) {
          if (input.length < 1) {
            return []
          }
          return Object.values(this.cryptoDict).filter(cryptoTicker => {
            return cryptoTicker
                .toLowerCase()
                .startsWith(input.toLowerCase())
          })
        },
        onSubmit(result){
          this.$emit('add-crypto',
              Object.keys(this.cryptoDict).find(key => this.cryptoDict[key] === result),
              'user_cryptos'
          )
        }
      },
      data(){
        return {
          cryptoDict: require('../crosswalk/crypto_dict.json')
        }
      },
  })
</script>

<style scoped>
  h3 {
    margin: 40px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
    border-radius: 8px;
  }

  #delete{
      background-color: #cc0000c2;
      border: none;
      color: white;
      padding: 7px 16px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 14px;
      margin: 2px 1px;
      cursor: pointer;
  }

  #add {
      background-color: #299006;
      border: none;
      color: white;
      padding: 7px 16px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 14px;
      margin: 2px 1px;
      cursor: pointer;
  }

  .grid {
    display: inline-table;
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

  #data {
    font-family: Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
  }

  #data td, #data th {
    border: 1px solid #ddd;
    padding: 8px;
  }

  #data tr:nth-child(even){background-color: #f2f2f2;}

  #data tr:hover {background-color: #ddd;}

  #data th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #d1a71d;
    color: white;
  }
</style>
