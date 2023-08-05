import styles from "./MoneyButton.module.css";

function MoneyButton({ rent_type, deposit, monthly }) {
  if (rent_type === "Monthly") {
    return (
      <span className={styles.moneyButton}>
        <span className={styles.moneyButtonText}>월세</span>
        <span className={styles.moneyButtonInt}>
          {deposit}/{monthly}
        </span>
      </span>
    );
  } else {
    return (
      <span className={styles.moneyButton}>
        <span className={styles.moneyButtonText}>전세</span>
        <span className={styles.moneyButtonInt}>{deposit}</span>
      </span>
    );
  }
}

export default MoneyButton;
