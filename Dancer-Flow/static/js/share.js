// // Pentagon
const myData = [
    [
        0.6119768296901937, 0.2724477365138749, 0.239318715565223, 0.8984415079405608, 0.6583948674656563
    ],
    [
        0.0949616836216769, 0.3719078227713477, 0.34293616595227383, 0.460621296000123, 0.7063279854775499
    ],
    [
        0.8504876012507432, 0.2653933980482446, 0.3178500882778421, 0.14247086217571958, 0.37765360881841503
    ],
    [
        0.5424735313476508, 0.8882713360214234, 0.17852702924856967, 0.9788178448900138, 0.42509719540882585
    ],
    [
        0.404222839154583, 0.05955589031331465, 0.45782102526548796, 0.5153100462187783, 0.17176626488842728
    ]
]

let sides = 5;

let el = document.getElementById("polygon-chart");

let chart = new window.PolygonChart({
  target: el,
  radius: 200,
  data: {
    data: myData,
    sides: sides,
    tooltips: {
      roundTo: 2,
      percentage: true,
    },
    colors: {
      normal: {
        polygonStroke: "#A54AE9",
        polygonFill: "#a54ae94f",
        pointStroke: "transparent",
        pointFill: "#A54AE9",
      },
      onHover: {
        polygonStroke: "#A54AE9",
        polyonFill: "#a54ae96f",
        pointStroke: "#A54AE9",
        pointFill: "#fff",
      },
    },
  },
  polygon: {
    colors: {
      normal: {
        fill: "#231E2C",
        stroke: "#3A255E",
      },
      onHover: {
        fill: "#231E2C",
        stroke: "#993DE0",
      }
    }
  },
  levels: {
    count: 5,
    labels: {
      enabled: true,
      position: {
        spline: 1,
        quadrant: 0,
      },
      colors: {
        normal: "#8B27D7",
        onHover: "#A54AE9",
      },
    },
  },
});
chart.init();