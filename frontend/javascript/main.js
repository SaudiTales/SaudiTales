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

//filter btn on expolre page
const filterbtn = document.querySelector(".filter-btn")
const optionslist = document.querySelector(".options-list")
const selectedtags = document.querySelector(".selected-tags")
//open menu
filterbtn.addEventListener("click", ()=>{
if (optionslist.style.display == "block"){
  optionslist.style.display = "none"
}
else{
  optionslist.style.display = "block"
}
})
//options
const options = document.querySelectorAll(".option")
//add event for options
options.forEach(option =>{
  option.addEventListener("click",()=>{
    let value = option.dataset.value;
    //not repeate options
    if (document.querySelector(`.tag[data-value="${value}"]`)){
      optionslist.style.display = "none"
      return;
    }
    //create the tags
    let tag = document.createElement("span");
    tag.classList.add("tag");
    tag.dataset.value = value;
    tag.innerHTML= `${value} <span class="remove-tag">&times;</span>`;

    selectedtags.appendChild(tag);

    optionslist.style.display = "none";
  });
});
//delete the tag
selectedtags.addEventListener("click", (e)=>{
  if (e.target.classList.contains("remove-tag")){
    e.target.parentElement.remove();
  }
});

//Image recognition section
document.addEventListener("DOMContentLoaded", () => {

  const imageinput = document.getElementById("ImageInput");
  const previewImage = document.getElementById("previewImage");
  const uploadText = document.getElementById("uploadText");
  const errorText = document.getElementById("errorText");
  const form = document.getElementById("imageSearchForm");

  imageinput.addEventListener("change",()=>{
    const file = imageinput.files[0];
    if (file){
      const reader = new FileReader();
      reader.onload =(e)=>{
        previewImage.src = e.target.result;
        uploadText.textContent = "Image uploaded";
        errorText.style.display = "none";
      };
      reader.readAsDataURL(file)
    }
  });

  // validate the form have an image before submit
  form.addEventListener("submit",(e)=>{
    const file = imageinput.files[0];
    if (!file){
      e.preventDefault();
      errorText.textContent = "Please upload an image before submitting!";
      errorText.style.display = "block";
      errorText.style.color = "red";
    } 
  });
});