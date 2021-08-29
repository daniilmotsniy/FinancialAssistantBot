// import logo from './logo.svg';
import './App.css';
import Asset from "./Asset";
import Assets from "./Assets";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/*<img src={logo} className="App-logo" alt="logo" />*/}
          <Asset asset='user_cryptos' color='rgb(209,167,29)'/>
          <Asset asset='user_stocks' color='rgb(87,168,60)'/>
          <Asset asset='user_currencies' color='rgb(80,60,168)'/>
          <Assets />
      </header>
    </div>
  );
}

export default App;
