import { Lobby } from "./components/lobby";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { GameInfo } from "./components/lobby/_components/game_info";
import { SecretHitlerHost } from "./components/secrethitler/_components/host";
import { SecretHitlerPlayer } from "./components/secrethitler/_components/players";

export default function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route exact path="/">
            <Lobby />
          </Route>
          <Route path="/lobby/:game_id" component={GameInfo} />
          <Route path="/u/lobby/:game_id/:user_id" component={GameInfo} />
          <Route path="/sh/:game_id" component={SecretHitlerHost} />{" "}
          {/* SH host play area */}
          <Route
            path="/u/sh/:game_id/:user_id"
            component={SecretHitlerPlayer}
          />{" "}
          {/* SH user play area */}
        </Switch>
      </div>
    </Router>
  );
}
