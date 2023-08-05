import { ReactComponent as GoodButtonImg } from "../../assets/Main/goodButtonImg.svg";
import { ReactComponent as BadButtonImg } from "../../assets/Main/badButtonImg.svg";

import styles from "./GoodButton.module.css";

function GoodButton() {
  return (
    <>
      <div className={styles.goodButtonFlex}>
        <div className={styles.redGood}>
          <GoodButtonImg className={styles.redGoodImg} />
          <span className={styles.redGoodSpan}>추천</span>
        </div>

        <div className={styles.blackBad}>
          <BadButtonImg className={styles.blackBadImg} />
          <span className={styles.blackBadSpan}>비추</span>
        </div>
      </div>
    </>
  );
}

export default GoodButton;
