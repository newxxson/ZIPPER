import { ReactComponent as GoodButtonImg } from "../../assets/Main/goodButtonImg.svg";
import { ReactComponent as BadButtonImg } from "../../assets/Main/badButtonImg.svg";
import styles from "./BadButton.module.css";

function BadButton() {
  return (
    <>
      <div className={styles.badButtonFlex}>
        <div className={styles.blackGood}>
          <GoodButtonImg className={styles.blackGoodImg} />
          <span className={styles.blackGoodSpan}>추천</span>
        </div>
        <br />
        <div className={styles.blueBad}>
          <BadButtonImg className={styles.blueBadImg} />
          <span className={styles.blueBadSpan}>비추</span>
        </div>
      </div>
    </>
  );
}

export default BadButton;
