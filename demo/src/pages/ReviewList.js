import styles from "./ReviewList.module.css";
import React, { useState, useEffect } from "react";
import OneReview from "../components/ReviewList/OneReview.js";
import reviewData from "../mock.json";
import Detail from "./Detail.js";
import ReviewAreaTitle from "../components/ReviewList/ReviewAreaTitle.js";

import { ReactComponent as GoodButtonImg } from "../assets/Main/goodButtonImg.svg";
import { ReactComponent as BadButtonImg } from "../assets/Main/badButtonImg.svg";
import { ReactComponent as LikeButton } from "../assets/Main/likeButton.svg";

const ReviewList = ({
  selectedHouse,
  setSelectedHouse,
  setMapInitial,
  isLiked,
  setIsLiked,
}) => {
  const [allReviews, setAllReviews] = useState([]);

  const [activeReview, setActiveReview] = useState(null);

  useEffect(() => {
    console.log("selectedHouse가 변경되었습니다:", selectedHouse);
  }, [selectedHouse]);

  useEffect(() => {
    console.log("isLiked가 변경되었습니다:", isLiked);
  }, [isLiked]);

  useEffect(() => {
    if (selectedHouse) {
      setIsLiked(selectedHouse.is_interested);
    }
  }, [selectedHouse]);

  useEffect(() => {
    if (!selectedHouse) return;

    const toAllReviews = reviewData.filter(
      (review) => review.address === selectedHouse.address
    );
    setAllReviews(toAllReviews);
  }, [selectedHouse]);

  const handleReviewClick = (review) => {
    setActiveReview(review);
  };

  const suggestRatio = selectedHouse ? selectedHouse.suggest_ratio : 0;
  const likeWidth = `${Math.max(suggestRatio, 0.01) * 100}%`;
  const dislikeWidth = `${Math.max(1 - suggestRatio, 0.01) * 100}%`;

  const goBack = () => {
    setSelectedHouse(null); // 선택된 주택 및 리뷰 초기화
    setMapInitial((prev) => !prev); // 지도 변경
  };

  //찜하기 버튼 컨트롤
  //찜 추가하기
  const addLike = async (houseId) => {
    const token = "6ccbf57b7dedbdaedbdc66851401bc9cde206ee0";
    try {
      const response = await fetch(
        "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/user-interest/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({
            house_pk: houseId,
          }), // 요청 바디를 JSON 문자열로 변환하여 전달
          mode: "cors",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to add like!");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  // 찜 취소 API 추가 (DELETE)
  const removeLike = async (houseId) => {
    const token = "6ccbf57b7dedbdaedbdc66851401bc9cde206ee0";
    try {
      const response = await fetch(
        `http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/user-interest/house/${houseId}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
          mode: "cors",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to remove like!");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleLikeButtonClick = async () => {
    const houseId = selectedHouse.id;

    if (!isLiked) {
      await addLike(houseId);
      setIsLiked(true);
      selectedHouse.is_interested = true;
    } else {
      await removeLike(houseId);
      setIsLiked(false);
      selectedHouse.is_interested = false;
    }
  };

  return (
    <div className={styles.div}>
      {selectedHouse ? (
        <>
          <div className={styles.likeButton}>
            <div
              className={styles.likeButtonDiv}
              onClick={handleLikeButtonClick}
            >
              <LikeButton fill={isLiked ? "#f44366" : "lightgray"} />
              <span className={styles.likeButtonSpan}>이 집 찜하기</span>
            </div>
          </div>

          <div className={styles.OneReviewHouseDiv}>
            <div className={styles.OneReviewHouseTitle}>
              <ReviewAreaTitle
                area_name={selectedHouse.area_name}
                className={styles.houseArea}
              />
              <span className={styles.houseAddress}>
                {selectedHouse.address}
              </span>
            </div>
            <div className={styles.OneReviewRatioTitle}>
              <span className={styles.ButtonSpan}>
                <GoodButtonImg fill="#4caf50" />
                <span className={styles.OneReviewLike}>추천</span>
              </span>
              <span className={styles.BadButtonSpan}>
                <BadButtonImg fill="#f44366" />
                <span className={styles.OneReviewDislike}>비추천</span>
              </span>
            </div>
            <div className={styles.ratioBar}>
              <div
                className={styles.ratioLike}
                style={{ width: likeWidth }}
              ></div>
              <div
                className={styles.ratioDislike}
                style={{ width: dislikeWidth }}
              ></div>
            </div>
          </div>
          <div className={styles.backButtonDiv}>
            <button onClick={goBack} className={styles.backButton}>
              목록으로 돌아가기
            </button>
          </div>
        </>
      ) : (
        <div>선택된 주택이 없습니다.</div>
      )}

      {allReviews.map((review, index) => (
        <div key={index} onClick={() => handleReviewClick(review)}>
          {activeReview && activeReview.id === review.id ? (
            <Detail selectedReview={review} setSelectedReview={null} />
          ) : (
            <OneReview review={review}></OneReview>
          )}
        </div>
      ))}
    </div>
  );
};

export default ReviewList;
