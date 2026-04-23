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
// add the landmarks to the table:
const bodyTable = document.getElementById("landmark-table")
function renderTable() {
    if (!bodyTable) return;
    bodyTable.innerHTML = ""

    landmarks.forEach((item, index) => {
        const row = document.createElement("tr")
        row.innerHTML = `
    <td>${item.id}</td>
    <td>${item.destination}</td>
    <td>${item.name}</td>
    <td>${item.description}</td>
    <td><img src="${item.image}" alt="landmark image" width=50px height=50px ></td>

    <td><button class="btn btn-danger deleteBtn" data-bs-toggle="modal" data-bs-target="#deleteLandmarkModal" data-index="${index}"><i class="bi bi-trash-fill"></i></button>
        <button class="btn btn-warning editBtn"  data-bs-toggle="modal" data-bs-target="#EditForm" data-index="${index}"><i class="bi bi-pencil-square"></i></button>
        </td>
    `
        bodyTable.appendChild(row)
    })
}
if (bodyTable) renderTable()


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
    const toast = bootstrap.Toast.getOrCreateInstance(toastEl)
    toast.show()


const confirmDeleteButton = document.getElementById("confirmDeleteLandmark")
if (confirmDeleteButton && deleteModal) {
    confirmDeleteButton.addEventListener("click", function () {
        if (deleteIndex !== null) {
            landmarks.splice(deleteIndex, 1)
            renderTable()
            const modal = bootstrap.Modal.getInstance(deleteModal)
            modal.hide()
            showToast("Landmark deleted successfully.", "success")
        }
    })
}

// add the users to the table:
const tabbody = document.getElementById("user-table")
function renderTable2() {
    if (!tabbody) return;
    tabbody.innerHTML = ""

    users.forEach((item, index) => {
        const row = document.createElement("tr")
        row.innerHTML = `
    <td>${item.id}</td>
    <td>${item.username}</td>
    <td>${item.name}</td>
    <td>${item.email}</td>
    <td>${item.accounttype}</td>
    <td>${item.status}</td>
    <td><button class="btn btn-danger deleteBtn" data-bs-toggle="modal" data-bs-target="#deleteUserModal" data-index="${index}"><i class="bi bi-trash-fill"></i></button>
                        <button class="btn btn-warning disableBtn" data-bs-toggle="modal" data-bs-target="#disableModal" data-index="${index}">Disable</button>
        </td>
    `
        tabbody.appendChild(row)
    })
}
if (tabbody) renderTable2()

// delete user
let deleteuser = null;

const deleteUserModal = document.getElementById("deleteUserModal")
if (deleteUserModal) {
    deleteUserModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget
        deleteuser = button.getAttribute("data-index")
    })
}

const confirmDeleteuser = document.getElementById("confirmDeleteUser")
if (confirmDeleteuser && deleteUserModal) {
    confirmDeleteuser.addEventListener("click", function () {
        if (deleteuser !== null) {
            users.splice(deleteuser, 1)
            renderTable2()
            const modal = bootstrap.Modal.getInstance(deleteUserModal)
            modal.hide()
            showToast("User deleted successfully.", "success")
        }
    })
}

// Search/Filter functionality for landmarks
const landmarkSearchInput = document.getElementById("landmarkSearchInput")
if (landmarkSearchInput) {
    landmarkSearchInput.addEventListener("keyup", function () {
        const searchText = this.value.toLowerCase()
        const tableRows = document.querySelectorAll("#landmark-table tr")
        
        tableRows.forEach(row => {
            const rowText = row.innerText.toLowerCase()
            if (rowText.includes(searchText)) {
                row.style.display = ""
            } else {
                row.style.display = "none"
            }
        })
    })
}

// Search/Filter functionality for users
const userSearchInput = document.getElementById("userSearchInput")
if (userSearchInput) {
    userSearchInput.addEventListener("keyup", function () {
        const searchText = this.value.toLowerCase()
        const tableRows = document.querySelectorAll("#user-table tr")
        
        tableRows.forEach(row => {
            const rowText = row.innerText.toLowerCase()
            if (rowText.includes(searchText)) {
                row.style.display = ""
            } else {
                row.style.display = "none"
            }
        })
    })
}
