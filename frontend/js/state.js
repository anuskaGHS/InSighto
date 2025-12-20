// frontend/js/state.js

const STATE_KEY = "insighto_dataset_id";

/**
 * Save dataset_id after successful upload
 */
function setDatasetId(datasetId) {
    localStorage.setItem(STATE_KEY, datasetId);
}

/**
 * Get stored dataset_id
 */
function getDatasetId() {
    return localStorage.getItem(STATE_KEY);
}

/**
 * Check if dataset exists
 */
function hasDataset() {
    return !!getDatasetId();
}

/**
 * Clear session (used when user finishes)
 */
function clearSession() {
    localStorage.removeItem(STATE_KEY);
}
