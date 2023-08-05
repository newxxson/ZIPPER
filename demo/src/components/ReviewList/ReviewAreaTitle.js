import styles from "./ReviewAreaTitle.module.css";

function ReviewAreaTitle({ area_name }) {
  return <span className={styles.areaButton}>{area_name}</span>;
}

export default ReviewAreaTitle;
