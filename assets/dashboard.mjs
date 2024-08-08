window.addEventListener("DOMContentLoaded", function () {
  const pathname = window.location.pathname;
  
  if (pathname === "/revenue") {
    setBackGroundColor("Revenue");
  } else if (pathname === "/ridership") {
    setBackGroundColor("Ridership");
  } else if (pathname === "/stock") {
    setBackGroundColor("Stock");
  } else if (pathname === "/hourly") {
    setBackGroundColor("Hourly Ridership");
  }
});

setBackGroundColor = (id) => {
  setTimeout(() => {
    const btn = document.getElementById(id);
    btn.style.background = "#2D9CDB";
  }, 1000);
};
