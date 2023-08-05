import Nav from "./components/Nav/Nav.js";
import styles from "./App.module.css";
import Map from "./components/Map/Map.js";
import ReviewList from "./pages/ReviewList.js";
import HouseList from "./pages/HouseList.js";
import Write from "./pages/Write.js";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";

import mockHouse2 from "./mock2.json";
import mockHouse3 from "./mock3.json";
import mockHouse4 from "./mock4.json";

const App = () => {
  const [houseData, setHouseData] = useState([]);
  const [likeHouseData, setLikeHouseData] = useState([]);
  const [townHouseData, setTownHouseData] = useState([]);
  const [mapInitial, setMapInitial] = useState(false);
  const [selectedHouse, setSelectedHouse] = useState(null);
  const [isLiked, setIsLiked] = useState(false);

  // //어느 경로에 있던지 새로고침하면 홈으로 돌아오도록 설정
  // useEffect(() => {
  //   const handleBeforeUnload = () => {
  //     window.location.href = "/";
  //   };

  //   window.addEventListener("beforeunload", handleBeforeUnload);

  //   return () => {
  //     window.removeEventListener("beforeunload", handleBeforeUnload);
  //   };
  // }, []);

  // //데이터 가져오기 Case1
  // useEffect(() => {
  //   setHouseData(mockHouse2);
  // }, []);

  // useEffect(() => {
  //   setLikeHouseData(mockHouse3);
  // }, []);

  // useEffect(() => {
  //   setTownHouseData(mockHouse4);
  // }, []);

  //데이터 가져오기 Case2
  const token = "6ccbf57b7dedbdaedbdc66851401bc9cde206ee0";

  const basicUrl =
    "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/houses?simple";
  const likeUrl =
    "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/user-interest/house";
  const townUrl =
    "http://ec2-13-125-213-208.ap-northeast-2.compute.amazonaws.com:8000/api/user-interest/area";

  async function fetchData(api, setData) {
    try {
      const response = await fetch(api, {
        method: "GET",
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
        mode: "cors",
      });

      const data = await response.json();
      setData(data);
    } catch (error) {
      console.log(error);
    }
  }

  useEffect(() => {
    fetchData(basicUrl, setHouseData);
  }, []);

  useEffect(() => {
    fetchData(likeUrl, setLikeHouseData);
  }, [isLiked]);

  useEffect(() => {
    fetchData(townUrl, setTownHouseData);
  }, []);

  return (
    <BrowserRouter>
      <div className={styles.divFlex}>
        <Nav className={styles.appNav} setMapInitial={setMapInitial} />
        <div className={styles.appBody}>
          <Routes>
            <Route path="/">
              <Route
                index
                element={
                  <HouseList
                    houseData={houseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                  />
                }
              />
              <Route
                path=":houseId"
                element={
                  selectedHouse ? (
                    <ReviewList
                      selectedHouse={selectedHouse}
                      setSelectedHouse={setSelectedHouse}
                      setMapInitial={setMapInitial}
                      isLiked={isLiked}
                      setIsLiked={setIsLiked}
                    />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
            </Route>

            <Route path="/write" element={<Write />} />

            <Route path="/like">
              <Route
                index
                element={
                  <HouseList
                    houseData={likeHouseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                  />
                }
              />
              <Route
                path=":houseId"
                element={
                  selectedHouse ? (
                    <ReviewList
                      selectedHouse={selectedHouse}
                      setSelectedHouse={setSelectedHouse}
                      setMapInitial={setMapInitial}
                      isLiked={isLiked}
                      setIsLiked={setIsLiked}
                    />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
            </Route>

            <Route path="/town">
              <Route
                index
                element={
                  <HouseList
                    houseData={townHouseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                  />
                }
              />
              <Route
                path=":houseId"
                element={
                  selectedHouse ? (
                    <ReviewList
                      selectedHouse={selectedHouse}
                      setSelectedHouse={setSelectedHouse}
                      setMapInitial={setMapInitial}
                      isLiked={isLiked}
                      setIsLiked={setIsLiked}
                    />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
            </Route>
          </Routes>
        </div>

        <div className={styles.appMap}>
          <Routes>
            <Route path="/">
              <Route
                index
                element={
                  <Map
                    houseData={houseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                    mapInitial={mapInitial}
                    setMapInitial={setMapInitial}
                  />
                }
              />
              <Route
                path=":houseId"
                element={
                  <Map
                    houseData={houseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                    mapInitial={mapInitial}
                    setMapInitial={setMapInitial}
                  />
                }
              />
            </Route>

            <Route path="/like">
              <Route
                index
                element={
                  <Map
                    houseData={likeHouseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                    mapInitial={mapInitial}
                    setMapInitial={setMapInitial}
                  />
                }
              />
              <Route
                path=":houseId"
                element={
                  <Map
                    houseData={likeHouseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                    mapInitial={mapInitial}
                    setMapInitial={setMapInitial}
                  />
                }
              />
            </Route>

            <Route path="/town">
              <Route
                index
                element={
                  <Map
                    houseData={townHouseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                    mapInitial={mapInitial}
                    setMapInitial={setMapInitial}
                  />
                }
              />
              <Route
                path=":houseId"
                element={
                  <Map
                    houseData={townHouseData}
                    selectedHouse={selectedHouse}
                    setSelectedHouse={setSelectedHouse}
                    mapInitial={mapInitial}
                    setMapInitial={setMapInitial}
                  />
                }
              />
            </Route>
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
};

export default App;
