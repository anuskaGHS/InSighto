// frontend/js/upload.js
console.log("upload.js loaded");

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const fileInput = document.querySelector('input[type="file"]');

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        console.log("Form submitted");


        if (!fileInput.files.length) {
            alert("Please select a file first.");
            return;
        }

        const file = fileInput.files[0];

        try {
            const result = await uploadDataset(file);
            console.log("Backend response:", result);

            if (result.status === "success") {
                setDatasetId(result.data.dataset_id);
                alert("File uploaded successfully!");
            } else {
                alert(result.message || "Upload failed.");
            }

        } catch (error) {
            alert("Server error. Please try again.");
            console.error(error);
        }
    });
});
