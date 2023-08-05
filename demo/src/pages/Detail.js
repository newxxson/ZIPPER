import styles from "./Detail.module.css";
import Stars from "../components/ReviewList/Stars.js";
import FloorButton from "../components/Detail/FloorButton.js";
import AreaButton from "../components/Detail/AreaButton.js";
import MoneyButton from "../components/Detail/MoneyButton.js";

import GoodButton from "../components/Detail/GoodButton.js";
import BadButton from "../components/Detail/BadButton.js";

function Detail({ selectedReview, setSelectedReview }) {
  return (
    <div className={styles.div}>
      {selectedReview ? (
        <div className={styles.detailReview}>
          <div className={styles.reviewTop}>
            <span className={styles.exitYear}>
              {selectedReview.exit_year}년까지 거주
            </span>
            <span className={styles.reviewSuggest}>
              {selectedReview.suggest ? <GoodButton /> : <BadButton />}
            </span>
          </div>

          <div className={styles.bigStarDiv}>
            <Stars
              className={styles.bigStar}
              rating={selectedReview.rating_overall}
              style={{ width: "17vw" }}
            />
          </div>

          <div className={styles.fourRating}>
            <div className={styles.row}>
              <div className={styles.rating}>
                <span className={styles.ratingTitle}>내부</span>
                <Stars
                  rating={selectedReview.rating_inside}
                  className={styles.ratingStar}
                  style={{ width: "7.5vw" }}
                />
              </div>
              <div className={styles.rating}>
                <span className={styles.ratingTitle}>교통</span>
                <Stars
                  rating={selectedReview.rating_transport}
                  className={styles.ratingStar}
                  style={{ width: "7.5vw" }}
                />
              </div>
            </div>
            <div className={styles.row}>
              <div className={styles.rating}>
                <span className={styles.ratingTitle}>인프라</span>
                <Stars
                  rating={selectedReview.rating_infra}
                  className={styles.ratingStar}
                  style={{ width: "7.5vw" }}
                />
              </div>
              <div className={styles.rating}>
                <span className={styles.ratingTitle}>안전</span>
                <Stars
                  rating={selectedReview.rating_safety}
                  className={styles.ratingStar}
                  style={{ width: "7.5vw" }}
                />
              </div>
            </div>
          </div>

          <div className={styles.reviewAddressInfo}>
            <AreaButton area={selectedReview.area} />

            <span className={styles.reviewAddress}>
              {selectedReview.address}
            </span>
          </div>

          <div className={styles.reviewMoneyInfo}>
            <span className={styles.reviewFloor}>
              <FloorButton
                floor={selectedReview.floor_type}
                className={styles.reviewFloorButton}
              />
            </span>
            <MoneyButton
              rent_type={selectedReview.rent_type}
              deposit={selectedReview.deposit}
              monthly={selectedReview.monthly}
            />
            <span className={styles.reviewMaintenance}>
              <span className={styles.reviewMaintenanceText}>관리비</span>
              <span className={styles.reviewMaintenanceInt}>
                {selectedReview.maintenance}
              </span>
            </span>
          </div>

          <div className={styles.reviewKeyword}>
            <div className={styles.keywordButtonsContainer}>
              {selectedReview.keyword.map((word, index) => (
                <span key={index} className={styles.keywordButton}>
                  {word}
                </span>
              ))}
            </div>
          </div>

          <div className={styles.reviewMerit}>
            <div className={styles.reviewMeritText}>
              실거주자가 알려주는 장점
            </div>
            <div className={styles.reviewMeritContent}>
              {selectedReview.merits}
            </div>
          </div>

          <div className={styles.reviewDemerit}>
            <div className={styles.reviewDemeritText}>
              실거주자가 알려주는 단점
            </div>
            <div className={styles.reviewDemeritContent}>
              {selectedReview.demerits}
            </div>
          </div>
        </div>
      ) : (
        <>
          <div>선택된 리뷰가 없습니다.</div>
        </>
      )}
    </div>
  );
}

export default Detail;
