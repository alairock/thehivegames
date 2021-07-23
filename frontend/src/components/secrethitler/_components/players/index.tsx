import { useEffect, useState } from "react";
import { Box, Button, Column, Columns, Modal } from "trunx";
import { Template } from "../template";
import { UserCard } from "../usercards";
import styles from "./players.module.scss";

export function SecretHitlerPlayer(props: any) {
  const [gameCode, setGameCode] = useState(props.match.params.game_id);
  const [users, setUsers] = useState<any>();
  const [myRole, setMyRole] = useState<any>();
  const [showRole, setShowRole] = useState<boolean>(false);
  const [user_id, setUser_id] = useState(props.match.params.user_id);
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
          user_id: user_id,
        }),
      });
      if (response.ok) {
        const r = await response.json();
        setUsers(r.roles);
        setMyRole(
          r.roles.filter((u: any) => u.user_id === user_id)[0]?.display_role
        );
      }
    })(gameCode);

    // SSE
    const sse = new EventSource(
      `/api/sh.events?lobby_code=${gameCode}&user_id=${user_id}`
    );
    sse.onmessage = (e) => handleSSEEvent(JSON.parse(e.data));
    sse.onerror = () => {
      sse.close();
    };

    return () => {
      sse.close();
    };
  }, []);

  const handleSSEEvent = (event: any) => {
    setGameState(event);
  };

  return (
    <Template>
      <Column>
        <Columns>
          <Column>
            SecretHitlerPlayer: {game_id}
            <br />
            <Button onClick={() => setShowRole(!showRole)}>Show Role</Button>
            <Modal isActive={showRole}>
              <Modal.Background onClick={() => setShowRole(!showRole)} />
              <Modal.Close onClick={() => setShowRole(!showRole)} isLarge />
              <Modal.Content className={styles.roleModal}>
                <Box>{myRole}</Box>
              </Modal.Content>
            </Modal>
          </Column>
        </Columns>
        <UserCard
          users={users}
          user_id={user_id}
          president_id={gameState?.president_id}
          chancellor_id={gameState?.chancellor_id}
        />
      </Column>
    </Template>
  );
}
