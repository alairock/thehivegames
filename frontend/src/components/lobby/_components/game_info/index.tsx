import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { Button, Column, Columns } from "trunx";
import { Template } from "../../../template";
import { ShowMembers } from "../members_list";
import styles from "./game_info.module.scss";

export const GameInfo = (props: any) => {
  const emptyGameState = {
    game: { status: "", game: "", min_players: 10, max_players: 10 },
    members: [],
  };
  const [maxPlayers, setMaxPlayers] = useState(10);
  const [minPlayers, setMinPlayers] = useState(5);
  const [gameState, setGameState] =
    useState<{ game: any; members: string[] }>(emptyGameState);
  const [gameCode, setGameCode] = useState<string>("");
  const [user_id, setUser_id] = useState<string>("");
  const history = useHistory();

  useEffect(() => {
    setGameCode(props.match.params.game_id);
    setUser_id(props.match.params.user_id);
    if (gameCode) {
      const sse = new EventSource(`/api/lobby.events?lobby_code=${gameCode}`);
      sse.onmessage = (e) => handleSSEEvent(JSON.parse(e.data));
      sse.onerror = () => {
        // error log here
        sse.close();
      };

      return () => {
        sse.close();
      };
    }
  }, [gameCode]);

  const handleSSEEvent = async (event: {
    game: {
      game: string;
      status: string;
      min_players: number;
      max_players: number;
    };
    members: string[];
    code: string;
    error: string;
  }) => {
    if (event?.game?.status === "in_progress") {
      if (user_id) {
        console.log("game in progress");
        // Show user play area
        history.push(`/u/${event?.game.game}/${gameCode}/${user_id}`);
      } else {
        // Show host play area
        history.push(`/${event?.game.game}/${gameCode}`);
      }
    }
    if (Object.keys(event).includes("code")) {
      console.log("error:", event.code, event.error);
      setGameState(emptyGameState);
    } else {
      setGameState(event);
      setMaxPlayers(event?.game?.max_players);
      setMinPlayers(event?.game?.min_players);
    }
  };

  async function leaveGame(user_id: string) {
    const response = await window.fetch("/api/lobby.leave", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        user_id: user_id,
        lobby_code: gameCode,
      }),
    });
    if (response.ok) {
      history.replace("/");
    }
  }

  async function startGame() {
    const response = await window.fetch("/api/game.start", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lobby_code: gameCode,
      }),
    });
    if (response.ok) {
      history.replace(`/sh/${gameCode}`);
    }
  }

  return (
    <Template>
      <Column>
        <Columns
          className={
            maxPlayers <= gameState?.members.length && !user_id
              ? styles.full
              : styles.bg
          }
        >
          <Column>
            <strong>
              GAME: {gameState.game.game == "SH" ? "Secret Hitler" : ""}
            </strong>
            <br />
            {maxPlayers <= gameState?.members.length && !user_id ? (
              <p className={styles.gameCode}>LOBBY FULL</p>
            ) : (
              <>
                Game Code: <p className={styles.gameCode}>{gameCode}</p>
              </>
            )}
            {user_id ? (
              <Button onClick={() => leaveGame(user_id)}>Leave</Button>
            ) : null}
            {!user_id && gameState?.members.length >= minPlayers ? (
              <Button onClick={() => startGame()}>Start</Button>
            ) : null}
          </Column>
        </Columns>
        <Columns>
          <Column>
            <ShowMembers members={gameState?.members} me={user_id} />
          </Column>
        </Columns>
      </Column>
    </Template>
  );
};
