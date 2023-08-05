import styles from "./FloorButton.module.css";

function FloorButton({ floor }) {
  if (floor === "UP") {
    return <span className={styles.floorButton}>고층</span>;
  } else if (floor === "MID") {
    return <span className={styles.floorButton}>중층</span>;
  } else if (floor === "DOWN") {
    return <span className={styles.floorButton}>저층</span>;
  }
}

export default FloorButton;
