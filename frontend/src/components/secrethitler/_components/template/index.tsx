import { Column, Columns } from "trunx";
import styles from "./template.module.scss";

export function Template(props: any) {
  return (
    <>
      <Columns className={styles.header}>
        <Column>Secret Hitler</Column>
      </Columns>
      <Columns className={styles.mainbody}>{props.children}</Columns>
      <Columns className={styles.footer}>
        <Column>©2021 The Hive Games</Column>
      </Columns>
    </>
  );
}
