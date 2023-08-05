import styles from "./AreaButton.module.css";

function Areabutton({ area }) {
  if (area === "Anam") {
    return <span className={styles.areaButton}>참살이길</span>;
  } else if (area === "Gangnam") {
    return <span className={styles.areaButton}>개운사길</span>;
  } else if (area === "Mapo") {
    return <span className={styles.areaButton}>법학관 후문</span>;
  } else {
    return <span className={styles.areaButton}>제기동</span>;
  }
}

export default Areabutton;
