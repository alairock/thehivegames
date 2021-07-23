import { useState } from "react";
import { Column, Input, Button, Label } from "trunx";
import styles from "./join_lobby.module.scss";
import { useHistory } from "react-router-dom";

export const JoinLobby = () => {
  const history = useHistory();
  const [gameCode, setGameCode] = useState<string>("");
  const [username, setUserName] = useState<string>("");

  const handleJoinGame = async (gameCode: any, username: any) => {
    if (username === "") return alert("Username is required");
    const response = await window.fetch("/api/lobby.join", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lobby_code: gameCode,
        username: username,
      }),
    });
    if (response.ok) {
      const x = await response.json();
      history.push(`/u/lobby/${gameCode}/${x.user_id}`);
    } else {
      alert("Invalid game code");
    }
  };
  return (
    <Column className={styles.join}>
      <div className={styles.header_banner}>Join</div>
      <Column>
        <Label>Username</Label>
        <Input
          onChange={(v) => setUserName(v.target.value)}
          value={username}
          placeholder={"Username"}
        />
        <Label>Game Code</Label>
        <Input
          className={styles.input}
          title="Game Code"
          placeholder={"eg: ABCD123"}
          onChange={(v) => setGameCode(v.target.value)}
          value={gameCode}
        />
        <Button
          className={styles.button}
          onClick={() => handleJoinGame(gameCode, username)}
        >
          Join
        </Button>
      </Column>
    </Column>
  );
};
