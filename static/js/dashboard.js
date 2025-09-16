// Dashboard JavaScript functionality

let attendanceChart = null;
let dashboardData = null;
let filteredStudents = [];

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadDashboardData();
    
    // Set up auto-refresh
    const dashboardRefresh = new EventManager.AutoRefresh(loadDashboardData, 15000);
    dashboardRefresh.start();
});

function initializeDashboard() {
    // Refresh button
    document.getElementById('refresh-dashboard').addEventListener('click', function() {
        loadDashboardData();
        EventManager.showToast('Dashboard refreshed', 'info');
    });
    
    // Export button
    document.getElementById('export-data').addEventListener('click', exportData);
    
    // Search functionality
    const searchInput = document.getElementById('search-students');
    const clearSearch = document.getElementById('clear-search');
    
    searchInput.addEventListener('input', function() {
        filterStudents(this.value);
    });
    
    clearSearch.addEventListener('click', function() {
        searchInput.value = '';
        filterStudents('');
    });
    
    // Initialize chart
    initializeChart();
}

function initializeChart() {
    const ctx = document.getElementById('attendanceChart').getContext('2d');
    
    attendanceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Scanned', 'Pending'],
            datasets: [{
                data: [0, 0],
                backgroundColor: [
                    '#28a745',
                    '#ffc107'
                ],
                borderWidth: 0,
                cutout: '60%'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                duration: 1000
            }
        }
    });
}

async function loadDashboardData() {
    try {
        const response = await EventManager.apiRequest('/api/dashboard_stats');
        dashboardData = response;
        updateDashboard(response);
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        EventManager.showToast('Failed to load dashboard data', 'error');
    }
}

function updateDashboard(data) {
    // Update statistics cards
    updateStatistics(data.stats);
    
    // Update chart
    updateChart(data.stats);
    
    // Update recent scans
    updateRecentScans(data.recent_scans);
    
    // Update students table
    updateStudentsTable(data.all_students);
}

function updateStatistics(stats) {
    document.getElementById('total-students').textContent = EventManager.formatNumber(stats.total_students);
    document.getElementById('scanned-count').textContent = EventManager.formatNumber(stats.scanned_count);
    document.getElementById('pending-count').textContent = EventManager.formatNumber(stats.pending_count);
    document.getElementById('completion-rate').textContent = `${stats.scan_percentage}%`;
}

function updateChart(stats) {
    if (attendanceChart) {
        attendanceChart.data.datasets[0].data = [stats.scanned_count, stats.pending_count];
        attendanceChart.update('none');
    }
}

function updateRecentScans(recentScans) {
    const container = document.getElementById('recent-scans');
    
    if (!recentScans || recentScans.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-clock fa-2x mb-2"></i>
                <p>No recent scans</p>
            </div>
        `;
        return;
    }
    
    const scansHTML = recentScans.map(scan => `
        <div class="d-flex justify-content-between align-items-center border-bottom py-2">
            <div>
                <div class="fw-bold">${scan.name}</div>
                <small class="text-muted">PRN: ${scan.prn}</small>
            </div>
            <div class="text-end">
                <span class="badge bg-success status-badge">✓</span>
                <br>
                <small class="text-muted">${EventManager.formatDate(scan.scanned_at)}</small>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = scansHTML;
}

function updateStudentsTable(students) {
    const tbody = document.getElementById('students-table-body');
    const countElement = document.getElementById('student-count');
    
    if (!students || students.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-4">
                    <i class="fas fa-users fa-2x mb-2"></i>
                    <p>No students found</p>
                </td>
            </tr>
        `;
        countElement.textContent = 'No students';
        return;
    }
    
    filteredStudents = students;
    renderStudentsTable(students);
    countElement.textContent = `Showing ${students.length} students`;
}

function renderStudentsTable(students) {
    const tbody = document.getElementById('students-table-body');
    
    const studentsHTML = students.map(student => {
        const statusClass = student.status === 'Scanned' ? 'bg-success' : 'bg-warning text-dark';
        const statusIcon = student.status === 'Scanned' ? 'fas fa-check' : 'fas fa-clock';
        
        return `
            <tr class="student-row">
                <td>
                    <div class="fw-bold">${student.name}</div>
                </td>
                <td>
                    <code>${student.prn}</code>
                </td>
                <td>
                    <a href="mailto:${student.email}" class="text-decoration-none">
                        ${student.email}
                    </a>
                </td>
                <td>
                    <span class="badge ${statusClass} status-badge">
                        <i class="${statusIcon} me-1"></i>${student.status}
                    </span>
                </td>
                <td>
                    ${student.scanned_at ? EventManager.formatDate(student.scanned_at) : '-'}
                </td>
            </tr>
        `;
    }).join('');
    
    tbody.innerHTML = studentsHTML;
}

function filterStudents(searchTerm) {
    if (!dashboardData || !dashboardData.all_students) return;
    
    const term = searchTerm.toLowerCase().trim();
    
    if (!term) {
        renderStudentsTable(dashboardData.all_students);
        document.getElementById('student-count').textContent = `Showing ${dashboardData.all_students.length} students`;
        return;
    }
    
    const filtered = dashboardData.all_students.filter(student => 
        student.name.toLowerCase().includes(term) ||
        student.prn.toLowerCase().includes(term) ||
        student.email.toLowerCase().includes(term) ||
        student.status.toLowerCase().includes(term)
    );
    
    renderStudentsTable(filtered);
    document.getElementById('student-count').textContent = `Showing ${filtered.length} of ${dashboardData.all_students.length} students`;
}

async function exportData() {
    try {
        // Show export modal
        const modal = new bootstrap.Modal(document.getElementById('exportModal'));
        modal.show();
        
        // Create a temporary link to download the file
        const response = await fetch('/api/export_data');
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `student_scan_report_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        // Hide modal
        modal.hide();
        
        EventManager.showToast('Data exported successfully', 'success');
        
    } catch (error) {
        console.error('Export failed:', error);
        EventManager.showToast('Failed to export data', 'error');
        
        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('exportModal'));
        if (modal) modal.hide();
    }
}

// Real-time updates using Server-Sent Events (if needed in future)
function initializeRealTimeUpdates() {
    if (typeof(EventSource) !== "undefined") {
        const eventSource = new EventSource('/api/events');
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            if (data.type === 'scan_update') {
                loadDashboardData();
                EventManager.showToast(`New scan: ${data.student_name}`, 'success');
            }
        };
        
        eventSource.onerror = function(event) {
            console.error('EventSource failed:', event);
        };
        
        // Close connection when page is unloaded
        window.addEventListener('beforeunload', function() {
            eventSource.close();
        });
    }
}

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page became visible, refresh data
        loadDashboardData();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R to refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        loadDashboardData();
        EventManager.showToast('Dashboard refreshed', 'info');
    }
    
    // Ctrl/Cmd + E to export
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        exportData();
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.getElementById('search-students');
        if (searchInput.value) {
            searchInput.value = '';
            filterStudents('');
        }
    }
});
