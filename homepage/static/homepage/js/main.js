const yearElement = document.getElementById("current-year");

if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

document.querySelectorAll(".alert").forEach((element) => {
    element.setAttribute("role", "alert");
});
