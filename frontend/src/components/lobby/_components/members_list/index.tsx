import { Content } from "trunx";

export const ShowMembers = ({ members, me }: any) => {
  return (
    <Content>
      <p>Users in Lobby</p>
      <ul>
        {members.map((m: any) => {
          if (m.id == me) {
            return (
              <li key={m.id}>
                <strong>{m.username} - YOU</strong>
              </li>
            );
          }
          return <li key={m.id}>{m.username}</li>;
        })}
      </ul>
    </Content>
  );
};
