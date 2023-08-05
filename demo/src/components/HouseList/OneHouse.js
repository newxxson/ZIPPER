import styles from "./OneHouse.module.css";
import Stars from "../ReviewList/Stars.js";
import AreaTitle from "./AreaTitle.js";

function OneHouse({ house }) {
  const suggestRatio = house.suggest_ratio || 0;
  const likeWidth = `${Math.max(suggestRatio, 0.01) * 100}%`;
  const dislikeWidth = `${Math.max(1 - suggestRatio, 0.01) * 100}%`;

  return (
    <span
      className={`${styles.oneHouse} ${
        house.user_like ? styles.userLiked : ""
      }`}
    >
      <AreaTitle areaName={house.area_name} userLike={house.user_like} />
      <span className={styles.houseAddress}>{house.address}</span>
      <Stars
        rating={house.rat_avg}
        style={{ width: "11vw", position: "absolute", bottom: "4vh" }}
      />
      <div className={styles.ratioBar}>
        <div className={styles.ratioLike} style={{ width: likeWidth }}></div>
        <div
          className={styles.ratioDislike}
          style={{ width: dislikeWidth }}
        ></div>
      </div>
    </span>
  );
}

export default OneHouse;
