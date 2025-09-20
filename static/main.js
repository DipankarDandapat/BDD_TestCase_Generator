// DOM elements
const generateBtn = document.getElementById('generateBtn');
const clearBtn = document.getElementById('clearBtn');
const requirementTextarea = document.getElementById('requirement');
const resultPre = document.getElementById('result');
const outputSection = document.getElementById('outputSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');
const btnText = document.querySelector('.btn-text');
const spinner = document.querySelector('.spinner');

// State
let currentFilename = null;

// Event listeners
generateBtn.addEventListener('click', generateBDD);
clearBtn.addEventListener('click', clearAll);
copyBtn.addEventListener('click', copyToClipboard);
downloadBtn.addEventListener('click', downloadFile);

// Auto-resize textarea
requirementTextarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
});

// Generate BDD test cases
async function generateBDD() {
    const requirement = requirementTextarea.value.trim();
    
    if (!requirement) {
        showError('Please enter a requirement description');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideError();
    hideOutput();
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ requirement })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showOutput(data.gherkin, data.filename);
            showToast('BDD test cases generated successfully!');
        } else {
            showError(data.error || 'Failed to generate BDD test cases');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        setLoadingState(false);
    }
}

// Clear all content
function clearAll() {
    requirementTextarea.value = '';
    hideOutput();
    hideError();
    requirementTextarea.style.height = 'auto';
    requirementTextarea.focus();
}

// Copy to clipboard
async function copyToClipboard() {
    try {
        await navigator.clipboard.writeText(resultPre.textContent);
        showToast('Copied to clipboard!');
        
        // Visual feedback
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        }, 2000);
    } catch (error) {
        showError('Failed to copy to clipboard');
    }
}

// Download file
function downloadFile() {
    if (currentFilename) {
        const link = document.createElement('a');
        link.href = `/download/${currentFilename}`;
        link.download = currentFilename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showToast('Download started!');
    }
}

// Show output section
function showOutput(gherkinText, filename) {
    resultPre.textContent = gherkinText;
    currentFilename = filename;
    outputSection.style.display = 'block';
    downloadBtn.style.display = 'flex';
    
    // Smooth scroll to output
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Hide output section
function hideOutput() {
    outputSection.style.display = 'none';
    currentFilename = null;
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    // Smooth scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Hide error
function hideError() {
    errorSection.style.display = 'none';
}

// Set loading state
function setLoadingState(isLoading) {
    if (isLoading) {
        generateBtn.disabled = true;
        btnText.style.display = 'none';
        spinner.style.display = 'block';
        generateBtn.classList.add('loading');
    } else {
        generateBtn.disabled = false;
        btnText.style.display = 'block';
        spinner.style.display = 'none';
        generateBtn.classList.remove('loading');
    }
}

// Show toast notification
function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!generateBtn.disabled) {
            generateBDD();
        }
    }
    
    // Escape to clear
    if (e.key === 'Escape') {
        clearAll();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    requirementTextarea.focus();
    
    // Add some example text if empty
    if (!requirementTextarea.value) {
        requirementTextarea.placeholder = `Describe your feature requirement in plain English...

Example:
As a user, I want to be able to login to the system using my email and password so that I can access my personal dashboard.

The system should validate the credentials and handle various scenarios like invalid email format, wrong password, account lockout, etc.`;
    }
});

// Health check on page load
fetch('/health')
    .then(response => response.json())
    .then(data => {
        console.log('Service status:', data.status);
    })
    .catch(error => {
        console.warn('Health check failed:', error);
    });

