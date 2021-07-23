import React, { useCallback, useEffect, useState } from "react";
import { Columns, Column, Content, Button } from "trunx";
import styles from "./secrethitler.module.scss";

export function SecretHitler({ playerId, gameCode, gameState }: any) {
  const [roles, setRoles] = useState<any>([]);
  const [users, setUsers] = useState<any>({});
  const cb = useCallback(handleGetPlayersInfo, [gameCode, playerId]);
  const cb2 = useCallback(handleGetUsersInfo, [gameCode]);
  useEffect(() => {
    cb();
    cb2();
    // handleGetUsersInfo();
  }, [cb, cb2]);

  async function handleGetPlayersInfo() {
    const response = await window.fetch("/api/sh.get_users", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lobby_code: gameCode,
        player_id: playerId,
      }),
    });
    if (response.ok) {
      const b: any = await response.json();
      setRoles(b.roles);
    }
  }

  async function handleGetUsersInfo() {
    const response = await window.fetch("/api/users.list", {
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
      setUsers(b.users);
    }
  }

  return (
    <Columns>
      <Column>
        <Columns>
          <Column>
            Me: {users[playerId]}
            <br />
            {roles?.map((p: any) => (
              <>
                order: {p.play_order}
                <RoleCard
                  me={playerId}
                  userId={p.user_id}
                  username={users[p.user_id]}
                  role={p.display_role}
                  gameState={gameState?.game?.state}
                  gameCode={gameCode}
                />
              </>
            ))}
          </Column>
        </Columns>
        <Columns>
          <Column>
            <QuitGame gameCode={gameCode} />
          </Column>
        </Columns>
      </Column>
    </Columns>
  );
}

const QuitGame = ({ gameCode }: any) => {
  async function handleQuitGame(_gameCode: string) {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const response = await window.fetch("/api/games.end", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lobby_code: _gameCode,
      }),
    });
  }
  return <Button onClick={() => handleQuitGame(gameCode)}>Quit</Button>;
};

const RoleCard = ({ me, userId, username, role, gameState, gameCode }: any) => {
  const president = gameState?.president_id;
  const presidentStyle = userId === president ? styles.president : null;
  const chancellor = gameState?.chancellor_id;
  const chancellorStyle = userId === chancellor ? styles.chancellor : null;
  const ineligible: boolean = gameState?.ineligible.includes(userId);
  const ineligibleStyle = ineligible ? styles.ineligible : null;

  async function handleSelectChancellor(gameCode: string, nominee: string) {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const response = await window.fetch("/api/sh.nominate_chancellor", {
      method: "POST",
      headers: {
        "content-type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify({
        lobby_code: gameCode,
        nominee: nominee,
      }),
    });
  }
  async function handleConfirm(gameCode: string) {
    console.log("confirm");
  }
  async function handleCancelNominee(gameCode: string) {
    console.log("cancel");
  }
  return (
    <Content
      className={[
        styles.roleCard,
        presidentStyle,
        ineligibleStyle,
        chancellorStyle,
      ].join(" ")}
    >
      Name: {username}
      <br />
      Role: {role}
      <br />
      {userId === president ? "President" : null}
      {userId === chancellor ? "Chancellor" : null}
      {me === president &&
      president !== userId &&
      !ineligible &&
      !chancellor ? (
        <Button onClick={() => handleSelectChancellor(gameCode, userId)}>
          Nominate
        </Button>
      ) : null}
      {me === president && chancellor === userId ? (
        <>
          <Button onClick={() => handleConfirm(gameCode)}>Confirm</Button>
          <Button onClick={() => handleCancelNominee(gameCode)}>Cancel</Button>
        </>
      ) : null}
    </Content>
  );
};
