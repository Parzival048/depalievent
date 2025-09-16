// Common JavaScript functions for Student Event Management System

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.getElementById('notification-toast');
    const toastBody = toast.querySelector('.toast-body');
    const toastHeader = toast.querySelector('.toast-header');
    
    // Set message
    toastBody.textContent = message;
    
    // Remove existing type classes
    toast.classList.remove('toast-success', 'toast-error', 'toast-warning', 'toast-info');
    
    // Add appropriate class
    toast.classList.add(`toast-${type}`);
    
    // Update header based on type
    const typeIcons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    
    const typeTexts = {
        success: 'Success',
        error: 'Error',
        warning: 'Warning',
        info: 'Information'
    };
    
    const icon = typeIcons[type] || typeIcons.info;
    const text = typeTexts[type] || typeTexts.info;
    
    toastHeader.innerHTML = `
        <i class="${icon} me-2"></i>
        <strong class="me-auto">${text}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    `;
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Loading state management
function setLoadingState(element, loading = true) {
    if (loading) {
        element.disabled = true;
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
        element.classList.add('loading');
    } else {
        element.disabled = false;
        element.classList.remove('loading');
    }
}

// API request helper
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// File upload helper
async function uploadFile(url, fileInput, progressCallback = null) {
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable && progressCallback) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressCallback(percentComplete);
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } catch (error) {
                    reject(new Error('Invalid response format'));
                }
            } else {
                try {
                    const error = JSON.parse(xhr.responseText);
                    reject(new Error(error.error || 'Upload failed'));
                } catch {
                    reject(new Error('Upload failed'));
                }
            }
        });
        
        xhr.addEventListener('error', () => {
            reject(new Error('Network error'));
        });
        
        xhr.open('POST', url);
        xhr.send(formData);
    });
}

// Format date helper with IST support
function formatDate(dateString) {
    if (!dateString) return 'N/A';

    try {
        // If it's already in IST format, return as is
        if (dateString.includes('IST')) {
            return dateString;
        }

        // Otherwise, convert to IST
        const date = new Date(dateString);
        return date.toLocaleString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZone: 'Asia/Kolkata',
            hour12: true
        }) + ' IST';
    } catch (error) {
        return dateString;
    }
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Copy to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (error) {
        console.error('Failed to copy:', error);
        showToast('Failed to copy to clipboard', 'error');
    }
}

// Download file helper
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Auto-refresh functionality
class AutoRefresh {
    constructor(callback, interval = 30000) {
        this.callback = callback;
        this.interval = interval;
        this.timer = null;
        this.isActive = false;
    }
    
    start() {
        if (this.isActive) return;
        
        this.isActive = true;
        this.timer = setInterval(() => {
            if (document.visibilityState === 'visible') {
                this.callback();
            }
        }, this.interval);
    }
    
    stop() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        this.isActive = false;
    }
    
    restart() {
        this.stop();
        this.start();
    }
}

// Initialize common functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Export functions for use in other scripts
window.EventManager = {
    showToast,
    setLoadingState,
    apiRequest,
    uploadFile,
    formatDate,
    formatNumber,
    isValidEmail,
    copyToClipboard,
    downloadFile,
    AutoRefresh
};
