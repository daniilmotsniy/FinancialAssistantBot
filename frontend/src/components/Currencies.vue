<template>
    <div>
        <h3>Here we have list of your currencies</h3>
        <br>
        <table id="data">
            <tr>
                <th>Currencie</th>
                <th>Delete</th>
            </tr>
            <tr v-for="i in user_currencies" :key="i">
                <td>{{ i }}</td>
                <td><a id="delete" v-on:click="$emit('remove-currencies', i)">Delete</a></td>
            </tr>
        </table>
        <br>
        <div class="grid">
          <input v-model="ticker" placeholder="type currencie ticker here">
          <a id="add" v-on:click="$emit('add-currencies', ticker)">Add currencie</a>
        </div>
        <br>
    </div>
</template>

<script>
  export default ({
      props: ['user_currencies']
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
    background-color: #57a83c;
    color: white;
  }
</style>
