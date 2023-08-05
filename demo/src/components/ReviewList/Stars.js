import { ReactComponent as StarImg } from "../../assets/Main/star.svg";
import styles from "./Stars.module.css";

function Stars({ rating, style }) {
  if (rating === 5) {
    return (
      <div className={styles.starDiv} style={style}>
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
      </div>
    );
  } else if (rating === 4) {
    return (
      <div className={styles.starDiv} style={style}>
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg />
      </div>
    );
  } else if (rating === 3) {
    return (
      <div className={styles.starDiv} style={style}>
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg />
        <StarImg />
      </div>
    );
  } else if (rating === 2) {
    return (
      <div className={styles.starDiv} style={style}>
        <StarImg className={styles.filled} />
        <StarImg className={styles.filled} />
        <StarImg />
        <StarImg />
        <StarImg />
      </div>
    );
  } else if (rating === 1) {
    return (
      <div className={styles.starDiv} style={style}>
        <StarImg className={styles.filled} />
        <StarImg />
        <StarImg />
        <StarImg />
        <StarImg />
      </div>
    );
  } else {
    return null; // Rating이 1~5 사이의 값이 아닐 경우에는 아무것도 렌더링하지 않음
  }
}

export default Stars;
