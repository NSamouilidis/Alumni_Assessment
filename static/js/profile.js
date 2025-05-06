/**
 * JavaScript file for profile page functionality
 */

document.addEventListener('DOMContentLoaded', () => {
    // Handle profile picture preview
    const profilePictureInput = document.getElementById('id_profile_picture');
    if (profilePictureInput) {
        profilePictureInput.addEventListener('change', function() {
            previewProfilePicture(this);
        });
    }

    // Toggle LinkedIn URL field based on whether a value exists
    const linkedinField = document.getElementById('id_linkedin_profile');
    if (linkedinField) {
        const linkedinFieldParent = linkedinField.closest('.mb-4');
        const linkedinToggleBtn = document.createElement('button');
        linkedinToggleBtn.type = 'button';
        linkedinToggleBtn.className = 'btn btn-sm btn-outline-secondary mt-1';
        linkedinToggleBtn.textContent = 'Add LinkedIn Profile';
        
        if (!linkedinField.value) {
            linkedinField.style.display = 'none';
            linkedinFieldParent.appendChild(linkedinToggleBtn);
            
            linkedinToggleBtn.addEventListener('click', () => {
                linkedinField.style.display = 'block';
                linkedinToggleBtn.style.display = 'none';
                linkedinField.focus();
            });
        }
    }

    // Form validation for LinkedIn URL
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const linkedinField = document.getElementById('id_linkedin_profile');
            if (linkedinField && linkedinField.value) {
                // Simple validation for LinkedIn URL
                if (!linkedinField.value.includes('linkedin.com')) {
                    e.preventDefault();
                    alert('Please enter a valid LinkedIn profile URL');
                    linkedinField.focus();
                }
            }
        });
    }

    // Initialize graduation year validation
    const graduationYearField = document.getElementById('id_graduation_year');
    if (graduationYearField) {
        graduationYearField.addEventListener('input', () => {
            const year = parseInt(graduationYearField.value);
            if (year && (year < 1950 || year > 2030)) {
                graduationYearField.setCustomValidity('Please enter a valid graduation year between 1950 and 2030.');
            } else {
                graduationYearField.setCustomValidity('');
            }
        });
    }
});

/**
 * Function to preview profile picture before upload
 */
function previewProfilePicture(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            // Find the profile image in the sidebar
            const profileImage = document.querySelector('.card-body img.rounded-circle');
            if (profileImage) {
                profileImage.src = e.target.result;
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}