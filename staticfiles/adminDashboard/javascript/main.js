// logout pop window 
const logoutModal = document.getElementById("modal-logout")
const closelogModal = document.getElementById("close-log-modal")

document.querySelectorAll(".logout-btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
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

// navbar
const menuBtn = document.getElementById("menu-btn");
const sidebar = document.getElementById("sidebar");
const navbar = document.getElementById("top-navbar");
const content = document.querySelector(".dashboard-content");

menuBtn.addEventListener("click", () => {
    sidebar.classList.toggle("closed");
    navbar.classList.toggle("shifted");
    content.classList.toggle("shifted");
});

// charts
const barColors = ["red", "green", "blue", "orange", "brown"];

document.addEventListener("DOMContentLoaded", () => {

    // Average Engagement
    new Chart(document.getElementById("engagementChart"), {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            datasets: [{
                label: "Average Engagement",
                data: [40, 55, 60, 70, 65, 80],
                borderColor: "#0B5D3B",
                backgroundColor: "rgba(11, 93, 59, 0.3)",
                borderWidth: 2,
                tension: 0.4
            }]
        }
    });

    // No.of viewed landmarks
    new Chart(document.getElementById("viewsChart"), {
        type: "bar",
        data: {
            labels: ["Riyadh Tower", "AlUla", "Diriyah", "Jeddah Corniche"],
            datasets: [{
                label: "Most Viewed Landmarks",
                data: [500, 350, 420, 300],
                backgroundColor: barColors
            }]
        }
    });

    // No.of visited
    new Chart(document.getElementById("visitsChart"), {
        type: "bar",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            datasets: [{
                label: "Number of Visits",
                data: [200, 180, 250, 300, 280, 350],
                backgroundColor: barColors
            }]
        }
    });

    // No.of most searched landmarks
    new Chart(document.getElementById("searchChart"), {
        type: "bar",
        data: {
            labels: ["AlUla", "Diriyah", "Edge of the World", "Masmak"],
            datasets: [{
                label: "Most Searched Landmarks",
                data: [150, 120, 180, 90],
                backgroundColor: barColors
            }]
        }
    });

    // most featured stories
    new Chart(document.getElementById("featuredChart"), {
        type: "pie",
        data: {
            labels: ["AlUla", "Diriyah", "Jeddah Corniche", "Riyadh Tower"],
            datasets: [{
                label: "Most Featured in Stories",
                data: [80, 60, 90, 70],
                backgroundColor: barColors
            }]
        }
    });

});


// delete landmark
let deleteIndex = null;

const deleteModal = document.getElementById("deleteLandmarkModal")
if (deleteModal) {
    deleteModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget
        deleteIndex = button.getAttribute("data-index")
    })
}

function showToast(message, type = "success") {
    const toastEl = document.getElementById("deleteToast")
    if (!toastEl) return

    toastEl.querySelector(".toast-body").textContent = message
    toastEl.classList.remove("text-bg-success", "text-bg-danger", "text-bg-warning")
    toastEl.classList.add(`text-bg-${type}`)

    deleteId = button.getAttribute("data-id")

}

// confirm the deleting
document.getElementById("confirmDelete").addEventListener("click", function(){

    if(deleteId){
        window.location.href = `/delete-landmark/${deleteId}/`;
    }

})
