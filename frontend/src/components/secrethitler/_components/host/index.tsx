import { useEffect, useState } from "react";
import { Button, Column, Columns } from "trunx";
import { Template } from "../template";
import { UserCard } from "../usercards";

export function SecretHitlerHost(props: any) {
  const [gameCode, setGameCode] = useState(props.match.params.game_id);
  const [users, setUsers] = useState(props.match.params.users);
  const [gameState, setGameState] = useState<any>();
  const game_id = props.match.params.game_id;

  useEffect(() => {
    // Get users
    (async function getUsers(lobby_code: string) {
      const response = await window.fetch("/api/sh.get_users", {
        method: "POST",
        headers: {
          "content-type": "application/json;charset=UTF-8",
        },
        body: JSON.stringify({
          lobby_code: gameCode,
        }),
      });
      if (response.ok) {
        const r = await response.json();
        setUsers(r.roles);
      }
    })(gameCode);

    // SSE
    const sse = new EventSource(`/api/sh.events?lobby_code=${gameCode}`);
    sse.onmessage = (e) => handleSSEEvent(JSON.parse(e.data));
    sse.onerror = () => {
      sse.close();
    };

    return () => {
      sse.close();
    };
  }, []);

  const handleSSEEvent = (event: any) => {
    console.log(event);
    setGameState(event);
  };

  const handleEndGame = async () => {
    const response = await window.fetch("/api/game.end", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lobby_code: gameCode,
      }),
    });
    if (response.ok) {
      const b: any = await response.json();
      console.log(b);
    }
  };

  return (
    <Template>
      <Column>
        <Columns>
          <Column>
            SecretHitlerHost: {game_id}
            <br />
            <Button onClick={() => handleEndGame()}>End Game</Button>
          </Column>
        </Columns>
        <UserCard
          users={users}
          president_id={gameState?.president_id}
          chancellor_id={gameState?.chancellor_id}
        />
      </Column>
    </Template>
  );
}
