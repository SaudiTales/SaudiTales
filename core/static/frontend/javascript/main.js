document.addEventListener("DOMContentLoaded", () => {

  //menu:
  const offcanvasEl = document.getElementById('navbarMenu');
  offcanvasEl.addEventListener('show.bs.offcanvas', () => {
    console.log('Menu opened');
  });

  // home page animation: 
  const reveals = document.querySelectorAll('.reveal');
  function revealOnScroll() {
    reveals.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 100) {
        el.classList.add('active');
      }
    });
  }
  window.addEventListener('scroll', revealOnScroll);
  revealOnScroll();

  // pages animation
  window.addEventListener("load", () => {
    document.querySelectorAll(".fade-in").forEach((el, i) => {
      setTimeout(() => {
        el.classList.add("show");
      }, i * 150);
    });
  });

  // logout pop window 
  const logoutModal = document.getElementById("modal-logout")
  const closelogModal = document.getElementById("close-log-modal")

  document.querySelectorAll(".logout-btn").forEach(btn => {
      btn.addEventListener("click", function(e) {
          e.preventDefault();
          logoutModal.style.display = "flex";
      });
  });

  closelogModal.addEventListener("click", () => {
      logoutModal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
      if (e.target === logoutModal) {
          logoutModal.style.display = "none";
      }
  });

  // filter dropdown
  const filterBtn = document.querySelector(".filter-btn");
  const optionsList = document.querySelector(".options-list");
  const regionInput = document.getElementById("regionInput");
  const searchInput = document.getElementById("searchInput");

  if (filterBtn && optionsList) {
    filterBtn.addEventListener("click", () => {
      optionsList.style.display =
        optionsList.style.display === "block" ? "none" : "block";
    });
  }

  document.querySelectorAll(".option").forEach(option => {
    option.addEventListener("click", () => {
      const value = option.dataset.value;

      if (searchInput) searchInput.value = value;
      if (regionInput) regionInput.value = value;

      if (optionsList) optionsList.style.display = "none";
    });
  });

  // search validation
  const searchForm = document.querySelector(".search-form");

  if (!searchForm || !searchInput || !searchError) {
    console.log("Search elements not found");
    return;
  }

  searchForm.addEventListener("submit", (e) => {

    const query = searchInput.value.trim();

    if (query === "") {
      e.preventDefault();

      searchError.textContent = "Please enter a search term";
      searchError.style.display = "block";
      return;
    }

    if (query.length < 3) {
      e.preventDefault();

      searchError.textContent = "Minimum 3 characters required";
      searchError.style.display = "block";
      return;
    }

    searchError.style.display = "none";
  });

  // Hides the error when the user starts typing
  searchInput.addEventListener("input", () => {
    searchError.style.display = "none";
  });

  //Image recognition section
  const imageInput = document.getElementById("ImageInput");
  const previewImage = document.getElementById("previewImage");
  const uploadText = document.getElementById("uploadText");
  const errorText = document.getElementById("errorText");
  const imageForm = document.getElementById("imageSearchForm");

  if (imageInput) {
    imageInput.addEventListener("change", () => {
      const file = imageInput.files[0];

      if (file) {
        const reader = new FileReader();

        reader.onload = (e) => {
          if (previewImage) previewImage.src = e.target.result;
          if (uploadText) uploadText.textContent = "Image uploaded";
          if (errorText) errorText.style.display = "none";
        };

        reader.readAsDataURL(file);
      }
    });
  }
  // Form validation to ensure an image is uploaded before submission
  if (imageForm) {
    imageForm.addEventListener("submit", (e) => {
      if (!imageInput?.files[0]) {
        e.preventDefault();
        if (errorText) {
          errorText.textContent = "Please upload an image";
          errorText.style.display = "block";
        }
      }
    });
  }

});