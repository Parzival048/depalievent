// QR Scanner JavaScript functionality

let video = null;
let canvas = null;
let context = null;
let scanning = false;
let currentStream = null;
let cameras = [];
let currentCameraIndex = 0;

document.addEventListener('DOMContentLoaded', function() {
    initializeScanner();
    loadScanStats();
    loadScanHistory();
    
    // Set up auto-refresh for stats and history
    const statsRefresh = new EventManager.AutoRefresh(loadScanStats, 10000);
    const historyRefresh = new EventManager.AutoRefresh(loadScanHistory, 15000);
    
    statsRefresh.start();
    historyRefresh.start();
});

function initializeScanner() {
    video = document.getElementById('qr-video');
    canvas = document.createElement('canvas');
    context = canvas.getContext('2d');
    
    // Set up event listeners
    document.getElementById('start-scanner').addEventListener('click', startScanner);
    document.getElementById('stop-scanner').addEventListener('click', stopScanner);
    document.getElementById('switch-camera').addEventListener('click', switchCamera);
    document.getElementById('refresh-history').addEventListener('click', loadScanHistory);
    
    // Manual QR input form
    document.getElementById('manual-qr-form').addEventListener('submit', handleManualQRInput);
    
    // Get available cameras
    getCameras();
}

async function getCameras() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        cameras = devices.filter(device => device.kind === 'videoinput');
        
        if (cameras.length > 1) {
            document.getElementById('switch-camera').style.display = 'inline-block';
        }
    } catch (error) {
        console.error('Error getting cameras:', error);
    }
}

async function startScanner() {
    try {
        const constraints = {
            video: {
                facingMode: cameras.length > 0 ? undefined : 'environment',
                deviceId: cameras.length > 0 ? cameras[currentCameraIndex].deviceId : undefined,
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };
        
        currentStream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = currentStream;
        
        video.addEventListener('loadedmetadata', () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
        });
        
        // Show scanner interface
        document.getElementById('scanner-status').style.display = 'none';
        document.getElementById('scanner-container').style.display = 'block';
        document.getElementById('scanner-controls').style.display = 'block';
        document.getElementById('camera-error').style.display = 'none';
        
        // Start scanning
        scanning = true;
        scanQRCode();
        
        EventManager.showToast('Scanner started successfully', 'success');
        
    } catch (error) {
        console.error('Error starting scanner:', error);
        document.getElementById('camera-error').style.display = 'block';
        EventManager.showToast('Failed to access camera', 'error');
    }
}

function stopScanner() {
    scanning = false;
    
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
    }
    
    video.srcObject = null;
    
    // Hide scanner interface
    document.getElementById('scanner-container').style.display = 'none';
    document.getElementById('scanner-controls').style.display = 'none';
    document.getElementById('scanner-status').style.display = 'block';
    
    EventManager.showToast('Scanner stopped', 'info');
}

async function switchCamera() {
    if (cameras.length <= 1) return;
    
    currentCameraIndex = (currentCameraIndex + 1) % cameras.length;
    
    if (scanning) {
        stopScanner();
        setTimeout(startScanner, 500);
    }
}

function scanQRCode() {
    if (!scanning || !video.videoWidth || !video.videoHeight) {
        if (scanning) {
            requestAnimationFrame(scanQRCode);
        }
        return;
    }
    
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    
    const code = jsQR(imageData.data, imageData.width, imageData.height);
    
    if (code) {
        handleQRCodeDetected(code.data);
    }
    
    if (scanning) {
        requestAnimationFrame(scanQRCode);
    }
}

async function handleQRCodeDetected(qrData) {
    // Temporarily stop scanning to prevent multiple scans
    scanning = false;

    // Handle both URL format and direct hash
    let qrHash = qrData.trim();
    if (qrHash.startsWith('http')) {
        // Extract hash from URL format (for Google Lens scans)
        qrHash = qrHash.split('/').pop();
    }

    try {
        // Add visual feedback
        showScanFeedback();

        const response = await EventManager.apiRequest('/api/validate_qr', {
            method: 'POST',
            body: JSON.stringify({ qr_hash: qrHash })
        });
        
        if (response.valid) {
            showScanResult(response.student, 'success');
            EventManager.showToast(`Successfully scanned: ${response.student.name}`, 'success');
            
            // Update stats and history
            loadScanStats();
            loadScanHistory();
        } else {
            showScanResult(null, 'error', response.message);
            EventManager.showToast(response.message, 'error');
        }
        
    } catch (error) {
        showScanResult(null, 'error', error.message);
        EventManager.showToast(error.message, 'error');
    }
    
    // Resume scanning after a delay
    setTimeout(() => {
        scanning = true;
        scanQRCode();
    }, 2000);
}

function showScanFeedback() {
    // Add visual feedback for successful scan detection
    const overlay = document.querySelector('.scanner-overlay');
    overlay.style.borderColor = '#28a745';
    overlay.style.boxShadow = '0 0 20px rgba(40, 167, 69, 0.5)';
    
    setTimeout(() => {
        overlay.style.borderColor = 'rgba(255, 255, 255, 0.8)';
        overlay.style.boxShadow = 'none';
    }, 1000);
}

function showScanResult(student, type, message = '') {
    const resultContainer = document.getElementById('scan-result');
    
    if (type === 'success' && student) {
        resultContainer.innerHTML = `
            <div class="text-center">
                <div class="mb-3">
                    <i class="fas fa-check-circle fa-3x text-success"></i>
                </div>
                <h5 class="text-success">Scan Successful!</h5>
                <div class="mt-3">
                    <strong>${student.name}</strong><br>
                    <span class="text-muted">PRN: ${student.prn}</span><br>
                    <span class="text-muted">${student.email}</span>
                </div>
                <div class="mt-3">
                    <span class="badge bg-success">Attendance Recorded</span>
                </div>
            </div>
        `;
    } else {
        resultContainer.innerHTML = `
            <div class="text-center">
                <div class="mb-3">
                    <i class="fas fa-times-circle fa-3x text-danger"></i>
                </div>
                <h5 class="text-danger">Scan Failed</h5>
                <div class="mt-3">
                    <p class="text-muted">${message || 'Invalid or already used QR code'}</p>
                </div>
            </div>
        `;
    }
    
    // Reset result after 5 seconds
    setTimeout(() => {
        resultContainer.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-qrcode fa-3x mb-3"></i>
                <p>Ready to scan QR codes</p>
            </div>
        `;
    }, 5000);
}

async function loadScanStats() {
    try {
        const response = await EventManager.apiRequest('/api/dashboard_stats');
        updateScanStats(response.stats);
    } catch (error) {
        console.error('Failed to load scan stats:', error);
    }
}

function updateScanStats(stats) {
    document.getElementById('total-scanned').textContent = EventManager.formatNumber(stats.scanned_count);
    document.getElementById('total-pending').textContent = EventManager.formatNumber(stats.pending_count);
    document.getElementById('scan-rate').textContent = `${stats.scan_percentage}%`;
}

async function loadScanHistory() {
    try {
        const response = await EventManager.apiRequest('/api/dashboard_stats');
        updateScanHistory(response.recent_scans);
    } catch (error) {
        console.error('Failed to load scan history:', error);
    }
}

function updateScanHistory(recentScans) {
    const historyContainer = document.getElementById('scan-history');
    
    if (!recentScans || recentScans.length === 0) {
        historyContainer.innerHTML = `
            <div class="col-12 text-center text-muted">
                <i class="fas fa-clock fa-2x mb-2"></i>
                <p>No scans yet today</p>
            </div>
        `;
        return;
    }
    
    const historyHTML = recentScans.map(scan => `
        <div class="col-md-6 col-lg-4">
            <div class="scan-history-item bg-light p-3 border">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1">${scan.name}</h6>
                        <small class="text-muted">PRN: ${scan.prn}</small>
                    </div>
                    <span class="badge bg-success">✓</span>
                </div>
                <div class="mt-2">
                    <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>
                        ${EventManager.formatDate(scan.scanned_at)}
                    </small>
                </div>
            </div>
        </div>
    `).join('');
    
    historyContainer.innerHTML = historyHTML;
}

async function handleManualQRInput(e) {
    e.preventDefault();
    
    const qrInput = document.getElementById('manual-qr-input');
    const qrInputValue = qrInput.value.trim();

    if (!qrInputValue) {
        EventManager.showToast('Please enter a QR code hash or URL', 'warning');
        return;
    }

    // Handle both URL format and direct hash
    let qrHash = qrInputValue;
    if (qrInputValue.startsWith('http')) {
        // Extract hash from URL format (for Google Lens scans)
        qrHash = qrInputValue.split('/').pop();
    }

    try {
        const response = await EventManager.apiRequest('/api/validate_qr', {
            method: 'POST',
            body: JSON.stringify({ qr_hash: qrHash })
        });
        
        if (response.valid) {
            showScanResult(response.student, 'success');
            EventManager.showToast(`Successfully validated: ${response.student.name}`, 'success');
            
            // Update stats and history
            loadScanStats();
            loadScanHistory();
            
            // Close modal and reset form
            const modal = bootstrap.Modal.getInstance(document.getElementById('manualInputModal'));
            modal.hide();
            qrInput.value = '';
        } else {
            EventManager.showToast(response.message, 'error');
        }
        
    } catch (error) {
        EventManager.showToast(error.message, 'error');
    }
}

// Handle page visibility changes to pause/resume scanning
document.addEventListener('visibilitychange', function() {
    if (document.hidden && scanning) {
        scanning = false;
    } else if (!document.hidden && currentStream) {
        scanning = true;
        scanQRCode();
    }
});
