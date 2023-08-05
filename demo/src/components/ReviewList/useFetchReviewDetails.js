// src/hooks/useFetchReviewDetails.js
import { useEffect } from "react";

const useFetchReviewDetails = (selectedReview) => {
  useEffect(() => {
    const fetchReviewDetails = async (review) => {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(`세부 정보: ${review.address}`);
        }, 1000);
      });
    };

    const fetchDetails = async () => {
      if (selectedReview) {
        const details = await fetchReviewDetails(selectedReview);
      }
    };

    fetchDetails();
  }, [selectedReview]);
};

export default useFetchReviewDetails;
