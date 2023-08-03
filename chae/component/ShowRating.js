import React, { useState, useEffect } from "react";
import styles from './ShowRating.module.css';
import { ReactComponent as Car } from "../assets/Car.svg";

const ShowRating = ({ onPrev, onNext, ratingData }) => {
  const [ratings, setRatings] = useState({
    internal: 0,
    transport: 0,
    infra: 0,
    safety: 0,
    overall: 0,
    recommend: undefined,
  });

  useEffect(() => {
    if (ratingData) {
      setRatings((prevRatings) => ({
        ...prevRatings,
        ratingData,
      }));
    }
  }, [ratingData]);

  const handleRatingChange = (category, rating) => {
    setRatings((prevRatings) => ({
      ...prevRatings,
      [category]: rating,
    }));
  };

  const handleRecommend = (isRecommend) => {
    setRatings((prevRatings) => ({
      ...prevRatings,
      recommend: isRecommend,
    }));
  };

  const handleNext = () => {
    onNext(ratings);
  };

  const handlePrev = () => {
    onPrev();
  };

  return (
    <div className={styles.container}>
      <h1>별점 매기기</h1>
      <h2>내부 평가</h2>
      <RatingForm
        category="internal"
        rating={ratings.internal}
        onRatingChange={handleRatingChange}
      />

      <h2>교통 평가</h2>
      <RatingForm
        category="transport"
        rating={ratings.transport}
        onRatingChange={handleRatingChange}
      />

      <h2>인프라 평가</h2>
      <RatingForm
        category="infra"
        rating={ratings.infra}
        onRatingChange={handleRatingChange}
      />

      <h2>안전 평가</h2>
      <RatingForm
        category="safety"
        rating={ratings.safety}
        onRatingChange={handleRatingChange}
      />

      {/* New star-based rating for overall satisfaction */}
      <h2>전체 만족도</h2>
      <RatingForm
        category="overall"
        rating={ratings.overall}
        onRatingChange={handleRatingChange}
      />
      <div>
      <h3>이 집은 후배들에게 추천하나요?</h3>
      <div className={styles.recommendButtons}>
        <button
          onClick={() => handleRecommend(true)}
          className={ratings.recommend === true ? styles.selected : ""}>
          <h3>👍추천</h3>
        </button>
        <button
          onClick={() => handleRecommend(false)}
          className={ratings.recommend === false ? styles.selected : ""}>
          <h3>👎비추천</h3>
        </button>
      </div></div>

      
      <div className={styles.bottom}>
      <div className={styles.buttonWrapper}>
      <button className={styles.button} onClick={handlePrev}><h3>BACK</h3></button>
      <button className={styles.button} onClick={handleNext}><h3>POST</h3></button>
      </div>

      <Car />
      <div className={styles.bottomBox}>
        <h3>4단계</h3>
        <h4>거의 끝났어요!</h4>
      </div></div>
    </div>
  );
};

const RatingForm = ({ category, rating, onRatingChange }) => {
  const handleRatingClick = (selectedRating) => {
    onRatingChange(category, selectedRating);
  };

  return (
    <div>
      <span>
        {[...Array(5)].map((_, index) => {
          const filledStars = Math.floor(rating);
          const hasHalfStar = rating - filledStars === 1;
          const starColor =
            index < filledStars || hasHalfStar ? "orange" : "gray";

          return (
            <span
              key={index}
              onClick={() => handleRatingClick(index + 1)}
              style={{
                cursor: "pointer",
                color: starColor,
              }}
            >
              &#9733;
            </span>
          );
        })}
        <span> {rating} 점</span>
      </span>
    </div>
  );
};

export default ShowRating;
