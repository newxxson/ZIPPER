import React, { useState, useEffect } from "react";

// http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com
export default function ShowReview({ token, data }) {
  const { form1Data, keywordData, textReviewData, ratingData } = data;

  const keywordPk = keywordData.selectedKeywords.map((dicts) => dicts.pk);
  const formData = new FormData();

  const body = {
    area: form1Data.area,
    address: form1Data.address,
    lat: "12.1.1.1",
    lng: "14.1.1.1",
    name: form1Data.name,
    floor_type: form1Data.floor,
    exit_year: form1Data.moveOutYear,
    house_type: form1Data.residenceType,
    rent_type: "monthly",
    deposit: form1Data.deposit,
    monthly: form1Data.monthlyRent,
    maintenance: form1Data.maintenance,
    keywords: keywordPk,
    merits: textReviewData.satisfaction,
    demerits: textReviewData.disappointment,
    rating_inside: ratingData.internal,
    rating_transport: ratingData.transport,
    rating_infra: ratingData.infra,
    rating_safety: ratingData.safety,
    rating_overall: ratingData.overall,
    suggest: ratingData.recommend,
  };

  formData.append("json_data", JSON.stringify(body));
  formData.append("image_data", textReviewData.residencePhoto);

  const sendReivew = () => {
    const apiUrl =
      "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/reviews/";

    fetch(apiUrl, {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
      },
      body: formData,
      mode: "cors",
    })
      .then((response) => response.json())

      .catch((error) => console.log(error));
  };

  return (
    <div>
      <h1>send?</h1>
      <button onClick={sendReivew}>post</button>
    </div>
  );
}
