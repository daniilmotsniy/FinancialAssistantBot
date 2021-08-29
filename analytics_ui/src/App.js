// import logo from './logo.svg';
import './App.css';
import Asset from "./Asset";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/*<img src={logo} className="App-logo" alt="logo" />*/}
          <Asset asset='user_cryptos' color='rgb(0,192,0)'/>
          <Asset asset='user_stocks' color='rgb(163,0,0)'/>
          <Asset asset='user_currencies' color='rgb(163,233,0)'/>
      </header>
    </div>
  );
}

export default App;
