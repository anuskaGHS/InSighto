document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-links a");
    const datasetId = localStorage.getItem("insighto_dataset_id");

    navLinks.forEach(link => {
        const href = link.getAttribute("href");

        // Highlight active page
        if (currentPath.endsWith(href)) {
            link.classList.add("active");
        }

        // Handle locked pages
        if (link.classList.contains("locked")) {
            if (!datasetId) {
                // Redirect to upload if clicked
                link.addEventListener("click", (e) => {
                    e.preventDefault();
                    window.location.href = "/frontend/pages/upload.html";
                });
            } else {
                // Unlock if dataset exists
                link.classList.remove("locked");
            }
        }
    });
});
