import { useState } from "react";
import { Button, Checkbox, Column, Input, Label } from "trunx";
import styles from "./create_lobby.module.scss";
import { useHistory } from "react-router-dom";

export const CreateGameField = () => {
  const [cohost, setCohost] = useState(false);
  const [gameCode, setGameCode] = useState<string>("");
  const history = useHistory();

  async function handleCreateGame() {
    const response = await window.fetch("/api/lobby.create", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({}),
    });
    if (response.ok) {
      const x = await response.json();
      history.push(`/lobby/${x.lobby_code}`);
    }
  }

  async function handleJoinGame(gameCode: string) {
    history.push(`/lobby/${gameCode}`);
  }

  return (
    <Column className={styles.join}>
      <div className={styles.header_banner}>Host</div>
      <Column>
        <Checkbox checked={cohost} onChange={() => setCohost(!cohost)}>
          Join as Co-Host
        </Checkbox>
        {cohost ? (
          <>
            <Label>Game Code</Label>
            <Input
              placeholder={"eg: ABCD123"}
              value={gameCode}
              onChange={(v) => setGameCode(v.target.value)}
            />
          </>
        ) : null}
        <br />
        <Button
          onClick={() =>
            cohost ? handleJoinGame(gameCode) : handleCreateGame()
          }
        >
          Host Game
        </Button>
      </Column>
    </Column>
  );
  // if (gameState.members.length < gameState?.game?.min_players) return null;
  // return <Button onClick={() => handleStartGame()}>Start Game</Button>;
};
