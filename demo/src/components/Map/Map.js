import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Map.module.css";

import greenmarkerImg from "../../assets/Main/greenmarkerImg.svg";
import redmarkerImg from "../../assets/Main/redmarkerImg.svg";
import QuestionBubble from "./QuestionBubble.js";

function Map({
  houseData,
  selectedHouse,
  setSelectedHouse,
  mapInitial,
  setMapInitial,
}) {
  const mapElement = useRef(null);
  const [houses, setHouses] = useState([]);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [infoWindow, setInfoWindow] = useState(null);
  const navigate = useNavigate();

  const { naver } = window;

  // useEffect(() => {
  //   console.log("selectedHouse 변경됨:", selectedHouse);
  // }, [selectedHouse]);

  ////useEffect
  //네이버 지도 생성
  useEffect(() => {
    const location = new naver.maps.LatLng(37.58626, 127.02924);
    const topLeftLatLng = new naver.maps.LatLng(37.5989, 127.0102);
    const bottomRightLatLng = new naver.maps.LatLng(37.5716, 127.044);
    const bounds = new naver.maps.LatLngBounds(
      topLeftLatLng,
      bottomRightLatLng
    );
    const mapOptions = {
      center: location,
      zoom: 16,
      zoomControl: true,
      zoomControlOptions: {
        position: naver.maps.Position.TOP_RIGHT,
        animation: naver.maps.Animation.EASE,
      },
      minZoom: 16,
      maxZoom: 20,
      restriction: {
        latlngBounds: bounds,
        strictBounds: true,
      },
    };

    const newMap = new naver.maps.Map(mapElement.current, mapOptions);
    setMap(newMap);

    //지도 경계 범위 밖으로 드래그 되면 다시 센터로 돌아오도록
    naver.maps.Event.addListener(newMap, "dragend", function () {
      const mapCenter = newMap.getCenter();
      if (!bounds.hasLatLng(mapCenter)) {
        newMap.setCenter(location);
      }
    });
  }, []);

  //지도 상에 나타내야 할 집 리스트 생성
  useEffect(() => {
    if (houseData.length) {
      setHouses(houseData);
    }
  }, [houseData]);

  // 마커 생성과 지도에 표시
  useEffect(() => {
    if (houses.length && map) {
      removeAllMarkers(); // Move this line here
      const newMarkersList = houses.map((location) => createMarker(location));
      setMarkers(newMarkersList);
    }
  }, [houses, map]);

  /////////////////////////////////////////////////////////////////

  //마커 생성 코드
  const removeAllMarkers = () => {
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    setMarkers([]);
  };

  const createMarker = (house) => {
    removeAllMarkers();
    //마커 기본 설정

    const markerIconUrl =
      house.suggest_ratio >= 0.5 ? greenmarkerImg : redmarkerImg;

    const markerSize = new naver.maps.Size(30, 30);

    const marker = new naver.maps.Marker({
      map: map,
      title: house.address,
      position: new naver.maps.LatLng(house.lat, house.lng),
      icon: {
        url: markerIconUrl,
        scaledSize: markerSize,
      },
    });

    //마커 hover 또는 줌레벨 변경 시 크기 변경
    // overHandler 등록과 바인딩

    const overHandler = () => {
      let zoomLevel = map.getZoom();
      let currentIcon = marker.getIcon();
      let currentSize = currentIcon.scaledSize;

      if (zoomLevel < 20) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(
            currentSize.width * 1.2,
            currentSize.height * 1.2
          ),
        });
      }
    };

    // outHandler 등록과 바인딩
    const outHandler = () => {
      let zoomLevel = map.getZoom();
      let currentIcon = marker.getIcon();
      let currentSize = currentIcon.scaledSize;

      if (zoomLevel < 20) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(
            (currentSize.width * 5) / 6,
            (currentSize.height * 5) / 6
          ),
        });
      }
    };

    naver.maps.Event.addListener(marker, "mouseover", overHandler);
    naver.maps.Event.addListener(marker, "mouseout", outHandler);

    //줌 레벨에 따라 마커 사이즈 달라지도록
    const updateMarkerSize = () => {
      const zoomLevel = map.getZoom();

      if (zoomLevel >= 20) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(70, 70),
        });
      } else if (zoomLevel >= 19) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(60, 60),
        });
      } else if (zoomLevel >= 18) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(50, 50),
        });
      } else if (zoomLevel >= 17) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(40, 40),
        });
      } else if (zoomLevel >= 16) {
        marker.setIcon({
          url: markerIconUrl,
          scaledSize: new naver.maps.Size(30, 30),
        });
      }
    };

    naver.maps.Event.addListener(map, "zoom_changed", updateMarkerSize);

    naver.maps.Event.addListener(marker, "click", () => {
      setSelectedHouse(house);
    });

    return marker;
  };

  //정보창 생성 코드
  const openInfoWindow = (marker, house) => {
    const offsetX = 0; // X축 이동할 픽셀 수
    const offsetY = 8; // Y축 이동할 픽셀 수 (50px 위로 올라감)

    const markerPosition = marker.getPosition();

    // 마커의 position을 pixel 좌표로 변환
    const markerPixelPosition = map
      .getProjection()
      .fromCoordToOffset(markerPosition);

    // 원하는 위치에 오프셋을 적용
    const newMarkerPixelPosition = new naver.maps.Point(
      markerPixelPosition.x + offsetX,
      markerPixelPosition.y - offsetY
    );

    // 새 좌표로부터 실제 경도와 위도를 얻음
    const newPositionCoord = map
      .getProjection()
      .fromOffsetToCoord(newMarkerPixelPosition);

    // 지도의 중심을 옮겨 마커의 위치를 조정
    map.setCenter(newPositionCoord);

    const infoWindowColor = house.suggest_ratio >= 0.5 ? "#4caf50" : "#f44366";

    const infoWindow = new naver.maps.InfoWindow({
      content: `<div class="${styles.infoWindowClass}">
        <b>${house.address}</b>
        <br>
        </div>`,
      borderColor: `${infoWindowColor}`,
      borderWidth: 3,
    });

    setInfoWindow(infoWindow);

    //줌인 애니메이션 발생시 애니메이션 종료 후 info 열리도록, 아닌 경우 바로 info 열리도록
    if (map.getZoom() < 20) {
      map.setZoom(20, true);
      naver.maps.Event.once(map, "idle", () => {
        infoWindow.open(map, marker);
      });
    } else {
      infoWindow.open(map, marker);
    }
  };

  //UseEffect
  // SelectedHouse가 있을 때 해당 마커로 정보창 열기
  // 마커 클릭 시 클릭된 마커 정보창 열기 함수
  const handleMarkerClick = (house) => {
    const clickedMarker = markers.find((marker) =>
      marker.getPosition().equals(new naver.maps.LatLng(house.lat, house.lng))
    );
    if (clickedMarker) {
      openInfoWindow(clickedMarker, house);
      navigate("/:houseId");
    }
  };

  useEffect(() => {
    //selectedHouse 있을 때 handleMarkerClick 실행
    if (map && selectedHouse) {
      handleMarkerClick(selectedHouse);
    }
  }, [map, selectedHouse]);

  //드래그, 줌 변경 발생시 인포 리스트 닫힘
  useEffect(() => {
    if (map) {
      naver.maps.Event.addListener(map, "dragstart", () => {
        if (infoWindow) {
          infoWindow.close();
        }
      });

      naver.maps.Event.addListener(map, "zoom_changed", () => {
        if (infoWindow) {
          infoWindow.close();
        }
      });
    }
  }, [map, infoWindow]);

  useEffect(() => {
    if (map && mapInitial) {
      const initialZoom = 16;
      const initialLocation = new naver.maps.LatLng(37.58626, 127.02924);
      map.setCenter(initialLocation);
      map.setZoom(initialZoom);
      setMapInitial(false);
    }
  }, [map, mapInitial]);

  //Town 아이콘 만드는 코드
  //   useEffect(() => {
  //     function getTownMarkerPosition(town) {
  //       let totalLat = 0;
  //       let totalLng = 0;
  //       const townMarkers = locations.filter(
  //         (location) => location.town === town
  //       );
  //       const townMarkerCount = townMarkers.length;
  //       for (const location of townMarkers) {
  //         totalLat += location.lat;
  //         totalLng += location.lng;
  //       }

  //       const averageLat = totalLat / townMarkerCount;
  //       const averageLng = totalLng / townMarkerCount;
  //       return new naver.maps.LatLng(averageLat, averageLng);
  //     }

  //     const updateMarkers = () => {
  //       const zoomLevel = map.getZoom();

  //       for (let i = 0; i < markers.length; i++) {
  //         markers[i].setMap(null);
  //       }

  //       if (zoomLevel > 16) {
  //         const newMarkers = locations.map((location) => {
  //           return createMarker(location);
  //         });
  //         setMarkers(newMarkers);
  //       } else {
  //         const townMarkers = {};
  //         locations.forEach((location) => {
  //           if (!townMarkers[location.town]) {
  //             townMarkers[location.town] = [];
  //           }
  //           townMarkers[location.town].push(location);
  //         });

  //         const newMarkers = Object.keys(townMarkers).map((town) => {
  //           const townMarkerCount = townMarkers[town].length;

  //           const labelIcon = {
  //             content: `<div class=${markerStyles.townMarker}>${townMarkerCount}</div>`,
  //             anchor: new naver.maps.Point(10, 10),
  //           };

  //           const townMarker = new naver.maps.Marker({
  //             map: map,
  //             position: getTownMarkerPosition(parseInt(town)),
  //             icon: labelIcon,
  //             label: {
  //               content: townMarkerCount.toString(),
  //               color: "white",
  //             },
  //           });

  //           return townMarker;
  //         });

  //         setMarkers(newMarkers);
  //       }
  //     };

  //     if (map) {
  //       naver.maps.Event.addListener(map, "zoom_changed", updateMarkers);
  //       updateMarkers();
  //     }
  //   }, [locations, map]);

  return (
    <>
      <div ref={mapElement} className={styles.map}>
        <div className={styles.mapIcon}>
          <QuestionBubble />
        </div>
      </div>
    </>
  );
}

export default Map;
