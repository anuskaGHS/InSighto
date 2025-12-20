// frontend/js/api.js

const BASE_URL = "http://localhost:5000";

/**
 * Upload dataset file
 * @param {File} file
 */
async function uploadDataset(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${BASE_URL}/api/upload`, {
        method: "POST",
        body: formData
    });

    return response.json();
}

/**
 * Get dataset overview
 * @param {string} datasetId
 */
async function fetchOverview(datasetId) {
    const response = await fetch(
        `${BASE_URL}/api/overview?dataset_id=${datasetId}`
    );

    return response.json();
}

/**
 * Run analysis
 * @param {Object} payload
 */
async function runAnalysis(payload) {
    const response = await fetch(`${BASE_URL}/api/analysis`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    return response.json();
}

/**
 * Generate report
 * @param {Object} payload
 */
async function generateReport(payload) {
    const response = await fetch(`${BASE_URL}/api/report`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    return response.json();
}
