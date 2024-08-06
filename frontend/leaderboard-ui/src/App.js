import logo from './logo.svg';
import './App.css';
import { Leaderboard } from './Leaderboard';

function App() {
  return (
    <div className="App">
      <h3> Welcome to your favourite gaming leaderboard</h3>
      <p> Now time to see your leaderboards</p>
      <hr />
      <Leaderboard />
    </div>
  );
}

export default App;
