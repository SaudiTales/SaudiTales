document.addEventListener("DOMContentLoaded", function () {

  document.addEventListener("click", function (e) {
      const btn = e.target.closest(".mod-btn");

      if (!btn) return;

      console.log("button clicked");

      document.body.classList.toggle("dark");

      if (document.body.classList.contains("dark")) {
          localStorage.setItem("theme", "dark");
      } else {
          localStorage.setItem("theme", "light");
      }
  });

  // load saved theme
  if (localStorage.getItem("theme") === "dark") {
      document.body.classList.add("dark");
  }

});