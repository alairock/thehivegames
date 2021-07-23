import { useEffect, useState } from "react";
import { Column, Columns, Container } from "trunx";
import styles from "./usercards.module.scss";
export function UserCard(props: any): JSX.Element | null {
  const {
    users,
    user_id = null,
    president_id = null,
    chancellor_id = null,
  } = props;
  const [isPresident, setIsPresident] = useState(false);
  const [isChancellor, setIsChancellor] = useState(false);
  const [showRoles, setShowRoles] = useState(false);

  useEffect(() => {
    if (user_id === president_id) {
      setIsPresident(true);
    }
    if (user_id === chancellor_id) {
      setIsChancellor(true);
    }
  }, [president_id, chancellor_id]);

  if (!users) {
    return null;
  }
  return (
    <Columns
      className={`${styles.cardcontainer} ${user_id && styles.pointer}`}
      onClick={() => setShowRoles(!showRoles)}
    >
      {users.map((user: any) => {
        return (
          <Column
            className={`${styles.usercard} ${
              user.user_id == president_id ? styles.president : ""
            } ${
              user_id === user.user_id && user.user_id == president_id
                ? styles.youpres
                : ""
            } ${user_id && showRoles ? styles[user.display_role] : ""}`}
            key={user.user_id}
          >
            {user.username}
            <br />
            {user_id === user.user_id ? "YOU" : null}
            <br />
            {user_id && showRoles ? (
              user.display_role == "hitler" ? (
                <strong>hitler</strong>
              ) : null
            ) : null}
          </Column>
        );
      })}
    </Columns>
  );
}
