// Admin panel JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize admin panel
    initializeAdminPanel();
    loadSystemStatus();
    
    // Set up auto-refresh for system status
    const statusRefresh = new EventManager.AutoRefresh(loadSystemStatus, 30000);
    statusRefresh.start();
});

function initializeAdminPanel() {
    // File upload form
    const uploadForm = document.getElementById('uploadForm');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadProgress = document.getElementById('uploadProgress');
    
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('studentFile');
        if (!fileInput.files[0]) {
            EventManager.showToast('Please select a file', 'warning');
            return;
        }
        
        // Validate file type
        const fileName = fileInput.files[0].name.toLowerCase();
        if (!fileName.endsWith('.xlsx') && !fileName.endsWith('.xls') && !fileName.endsWith('.csv')) {
            EventManager.showToast('Please select an Excel or CSV file', 'error');
            return;
        }
        
        try {
            EventManager.setLoadingState(uploadBtn, true);
            uploadProgress.style.display = 'block';
            
            const response = await EventManager.uploadFile('/api/upload_students', fileInput, (progress) => {
                console.log(`Upload progress: ${progress}%`);
            });
            
            EventManager.showToast(response.message, 'success');
            uploadForm.reset();
            loadSystemStatus(); // Refresh status
            
        } catch (error) {
            EventManager.showToast(error.message, 'error');
        } finally {
            EventManager.setLoadingState(uploadBtn, false);
            uploadBtn.innerHTML = '<i class="fas fa-upload me-1"></i>Upload Students';
            uploadProgress.style.display = 'none';
        }
    });
    
    // Generate QR codes button
    const generateQRBtn = document.getElementById('generateQRBtn');
    const qrProgress = document.getElementById('qrProgress');
    
    generateQRBtn.addEventListener('click', async function() {
        try {
            EventManager.setLoadingState(generateQRBtn, true);
            qrProgress.style.display = 'block';
            
            const response = await EventManager.apiRequest('/api/generate_qr_codes', {
                method: 'POST'
            });
            
            EventManager.showToast(response.message, 'success');
            loadSystemStatus(); // Refresh status
            
        } catch (error) {
            EventManager.showToast(error.message, 'error');
        } finally {
            EventManager.setLoadingState(generateQRBtn, false);
            generateQRBtn.innerHTML = '<i class="fas fa-qrcode me-1"></i>Generate QR Codes';
            qrProgress.style.display = 'none';
        }
    });
    
    // Send emails button
    const sendEmailsBtn = document.getElementById('sendEmailsBtn');
    const emailProgress = document.getElementById('emailProgress');
    
    sendEmailsBtn.addEventListener('click', async function() {
        // Show confirmation dialog
        if (!confirm('Are you sure you want to send emails to all students? This action cannot be undone.')) {
            return;
        }
        
        try {
            EventManager.setLoadingState(sendEmailsBtn, true);
            emailProgress.style.display = 'block';
            
            const response = await EventManager.apiRequest('/api/send_emails', {
                method: 'POST'
            });
            
            EventManager.showToast(response.message, 'success');
            loadSystemStatus(); // Refresh status
            
        } catch (error) {
            EventManager.showToast(error.message, 'error');
            
            // Show email configuration modal if needed
            if (error.message.includes('Email configuration')) {
                const modal = new bootstrap.Modal(document.getElementById('emailConfigModal'));
                modal.show();
            }
        } finally {
            EventManager.setLoadingState(sendEmailsBtn, false);
            sendEmailsBtn.innerHTML = '<i class="fas fa-envelope me-1"></i>Send Emails';
            emailProgress.style.display = 'none';
        }
    });
    
    // Refresh status button
    const refreshStatusBtn = document.getElementById('refreshStatusBtn');
    refreshStatusBtn.addEventListener('click', function() {
        loadSystemStatus();
        EventManager.showToast('Status refreshed', 'info');
    });

    // Clear data functionality
    setupClearDataFunctionality();
}

async function loadSystemStatus() {
    try {
        const response = await EventManager.apiRequest('/api/dashboard_stats');
        updateSystemStatus(response);
    } catch (error) {
        console.error('Failed to load system status:', error);
        document.getElementById('systemStatus').innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle me-1"></i>
                Failed to load system status
            </div>
        `;
    }
}

function updateSystemStatus(data) {
    const statusContainer = document.getElementById('systemStatus');
    const stats = data.stats;
    
    statusContainer.innerHTML = `
        <div class="row g-3">
            <div class="col-6">
                <div class="text-center">
                    <div class="h4 text-primary mb-0">${EventManager.formatNumber(stats.total_students)}</div>
                    <small class="text-muted">Total Students</small>
                </div>
            </div>
            <div class="col-6">
                <div class="text-center">
                    <div class="h4 text-success mb-0">${EventManager.formatNumber(stats.scanned_count)}</div>
                    <small class="text-muted">Scanned</small>
                </div>
            </div>
            <div class="col-6">
                <div class="text-center">
                    <div class="h4 text-warning mb-0">${EventManager.formatNumber(stats.pending_count)}</div>
                    <small class="text-muted">Pending</small>
                </div>
            </div>
            <div class="col-6">
                <div class="text-center">
                    <div class="h4 text-info mb-0">${stats.scan_percentage}%</div>
                    <small class="text-muted">Completion</small>
                </div>
            </div>
        </div>
        <div class="mt-3">
            <div class="progress" style="height: 10px;">
                <div class="progress-bar bg-success" style="width: ${stats.scan_percentage}%"></div>
            </div>
        </div>
    `;
    
    // Update recent activity
    updateRecentActivity(data.recent_scans);
}

function updateRecentActivity(recentScans) {
    const activityContainer = document.getElementById('recentActivity');
    
    if (!recentScans || recentScans.length === 0) {
        activityContainer.innerHTML = '<p class="text-muted">No recent activity</p>';
        return;
    }
    
    const activityHTML = recentScans.map(scan => `
        <div class="d-flex justify-content-between align-items-center border-bottom py-2">
            <div>
                <strong>${scan.name}</strong>
                <br>
                <small class="text-muted">PRN: ${scan.prn}</small>
            </div>
            <div class="text-end">
                <span class="badge bg-success">Scanned</span>
                <br>
                <small class="text-muted">${EventManager.formatDate(scan.scanned_at)}</small>
            </div>
        </div>
    `).join('');
    
    activityContainer.innerHTML = activityHTML;
}

// File drag and drop functionality
function setupFileDragDrop() {
    const fileInput = document.getElementById('studentFile');
    const uploadForm = document.getElementById('uploadForm');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadForm.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadForm.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadForm.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        uploadForm.classList.add('dragover');
    }
    
    function unhighlight(e) {
        uploadForm.classList.remove('dragover');
    }
    
    uploadForm.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            EventManager.showToast('File selected for upload', 'info');
        }
    }
}

// Initialize drag and drop when page loads
document.addEventListener('DOMContentLoaded', setupFileDragDrop);

function setupClearDataFunctionality() {
    const confirmationInput = document.getElementById('confirmationInput');
    const confirmClearBtn = document.getElementById('confirmClearBtn');
    const clearDataForm = document.getElementById('clearDataForm');

    // Enable/disable confirm button based on input
    confirmationInput.addEventListener('input', function() {
        const isValid = this.value.trim() === 'CLEAR_ALL_DATA';
        confirmClearBtn.disabled = !isValid;

        if (isValid) {
            confirmClearBtn.classList.remove('btn-danger');
            confirmClearBtn.classList.add('btn-outline-danger');
        } else {
            confirmClearBtn.classList.remove('btn-outline-danger');
            confirmClearBtn.classList.add('btn-danger');
        }
    });

    // Handle clear data confirmation
    confirmClearBtn.addEventListener('click', async function() {
        const confirmation = confirmationInput.value.trim();

        if (confirmation !== 'CLEAR_ALL_DATA') {
            EventManager.showToast('Invalid confirmation text', 'error');
            return;
        }

        // Final confirmation dialog
        if (!confirm('Are you absolutely sure you want to delete ALL data? This action cannot be undone!')) {
            return;
        }

        try {
            EventManager.setLoadingState(confirmClearBtn, true);

            const response = await EventManager.apiRequest('/api/clear_all_data', {
                method: 'POST',
                body: JSON.stringify({ confirmation: confirmation })
            });

            if (response.success) {
                EventManager.showToast(response.message, 'success');

                // Close modal and reset form
                const modal = bootstrap.Modal.getInstance(document.getElementById('clearDataModal'));
                modal.hide();
                confirmationInput.value = '';
                confirmClearBtn.disabled = true;

                // Refresh system status
                loadSystemStatus();

                // Show success details
                setTimeout(() => {
                    const details = response.cleared;
                    EventManager.showToast(
                        `Cleared: ${details.students} students, ${details.scans} scans, QR files, and uploads`,
                        'info'
                    );
                }, 1000);

            } else {
                EventManager.showToast(response.error || 'Failed to clear data', 'error');
            }

        } catch (error) {
            EventManager.showToast(error.message, 'error');
        } finally {
            EventManager.setLoadingState(confirmClearBtn, false);
            confirmClearBtn.innerHTML = '<i class="fas fa-trash-alt me-1"></i>Delete All Data';
        }
    });

    // Reset form when modal is hidden
    document.getElementById('clearDataModal').addEventListener('hidden.bs.modal', function() {
        confirmationInput.value = '';
        confirmClearBtn.disabled = true;
        confirmClearBtn.classList.remove('btn-outline-danger');
        confirmClearBtn.classList.add('btn-danger');
    });
}
