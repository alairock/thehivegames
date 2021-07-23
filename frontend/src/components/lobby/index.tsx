import React, { useState } from "react";
import { JoinLobby } from "./_components/join_lobby";
import { CreateGameField } from "./_components/create_lobby";
import { Template } from "../template";

export function Lobby() {
  return (
    <Template>
      <JoinLobby />
      <CreateGameField />
    </Template>
  );
}
