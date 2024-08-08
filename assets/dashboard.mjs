window.addEventListener("DOMContentLoaded", function () {
  const pathname = window.location.pathname;
console.log({pathname})
  if (pathname === "/revenue") {
    console.log("reve");
    const btn = document.getElementById("Revenue");
    console.log(btn);
  }

});
