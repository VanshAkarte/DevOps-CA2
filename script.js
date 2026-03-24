/**
 * script.js – JavaScript Form Validation
 * Student Feedback Registration Form
 * DevOps CA2 Project
 */

'use strict';

// ──────────────────────────────────────────────
// Word-count live updater for Comments textarea
// ──────────────────────────────────────────────
document.getElementById('comments').addEventListener('input', function () {
  const wordCount = countWords(this.value);
  const hint = document.getElementById('wordCount');
  hint.textContent = `Words: ${wordCount} / 10 minimum`;
  hint.style.color = wordCount >= 10 ? '#6ee7b7' : '#94a3b8';
});

// ──────────────────────────────────────────────
// Main form submit handler
// ──────────────────────────────────────────────
document.getElementById('feedbackForm').addEventListener('submit', function (e) {
  e.preventDefault();
  if (validateForm()) {
    showSuccess();
  }
});

// ──────────────────────────────────────────────
// Core validation function
// Returns true if ALL validations pass
// ──────────────────────────────────────────────
function validateForm() {
  clearErrors();
  let isValid = true;

  // 1. Student Name – must not be empty
  const name = document.getElementById('studentName').value.trim();
  if (!name) {
    showError('studentName', 'nameError', 'Student name is required.');
    isValid = false;
  } else if (name.length < 2) {
    showError('studentName', 'nameError', 'Name must be at least 2 characters.');
    isValid = false;
  } else {
    markValid('studentName');
  }

  // 2. Email – must match standard email format
  const email = document.getElementById('email').value.trim();
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) {
    showError('email', 'emailError', 'Email address is required.');
    isValid = false;
  } else if (!emailRegex.test(email)) {
    showError('email', 'emailError', 'Please enter a valid email (e.g. user@domain.com).');
    isValid = false;
  } else {
    markValid('email');
  }

  // 3. Mobile Number – exactly 10 digits
  const mobile = document.getElementById('mobile').value.trim();
  const mobileRegex = /^\d{10}$/;
  if (!mobile) {
    showError('mobile', 'mobileError', 'Mobile number is required.');
    isValid = false;
  } else if (!mobileRegex.test(mobile)) {
    showError('mobile', 'mobileError', 'Mobile number must be exactly 10 digits (numbers only).');
    isValid = false;
  } else {
    markValid('mobile');
  }

  // 4. Department – must have a selection
  const dept = document.getElementById('department').value;
  if (!dept) {
    showError('department', 'deptError', 'Please select your department.');
    isValid = false;
  } else {
    markValid('department');
  }

  // 5. Gender – at least one radio must be selected
  const genderSelected = document.querySelector('input[name="gender"]:checked');
  if (!genderSelected) {
    document.getElementById('genderError').textContent = 'Please select your gender.';
    isValid = false;
  } else {
    document.getElementById('genderError').textContent = '';
  }

  // 6. Feedback Comments – not blank AND at least 10 words
  const comments = document.getElementById('comments').value.trim();
  const wordCount = countWords(comments);
  if (!comments) {
    showError('comments', 'commentsError', 'Feedback comments are required.');
    isValid = false;
  } else if (wordCount < 10) {
    showError('comments', 'commentsError',
      `Comments must be at least 10 words. Current: ${wordCount} word${wordCount === 1 ? '' : 's'}.`);
    isValid = false;
  } else {
    markValid('comments');
  }

  return isValid;
}

// ──────────────────────────────────────────────
// Helper: count words in a string
// ──────────────────────────────────────────────
function countWords(text) {
  const trimmed = text.trim();
  if (!trimmed) return 0;
  return trimmed.split(/\s+/).length;
}

// ──────────────────────────────────────────────
// Helper: show error state on a field
// ──────────────────────────────────────────────
function showError(fieldId, errorId, message) {
  const field = document.getElementById(fieldId);
  const error = document.getElementById(errorId);
  if (field) {
    field.classList.remove('input-valid');
    field.classList.add('input-error');
  }
  if (error) error.textContent = message;
}

// ──────────────────────────────────────────────
// Helper: mark a field as valid
// ──────────────────────────────────────────────
function markValid(fieldId) {
  const field = document.getElementById(fieldId);
  if (field) {
    field.classList.remove('input-error');
    field.classList.add('input-valid');
  }
}

// ──────────────────────────────────────────────
// Helper: clear all errors and valid states
// ──────────────────────────────────────────────
function clearErrors() {
  const errorSpans = document.querySelectorAll('.error-msg');
  errorSpans.forEach(span => (span.textContent = ''));

  const allFields = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], select, textarea');
  allFields.forEach(field => {
    field.classList.remove('input-error', 'input-valid');
  });

  // Hide success banner
  document.getElementById('successBanner').style.display = 'none';
}

// ──────────────────────────────────────────────
// Show success confirmation banner
// ──────────────────────────────────────────────
function showSuccess() {
  const name = document.getElementById('studentName').value.trim();
  const dept = document.getElementById('department').value;

  const msg = `Thank you, ${name}! Your feedback for the ${dept} department has been recorded.`;
  document.getElementById('successMessage').textContent = msg;

  const banner = document.getElementById('successBanner');
  banner.style.display = 'flex';
  banner.scrollIntoView({ behavior: 'smooth', block: 'start' });

  // Reset form after short delay
  setTimeout(() => {
    document.getElementById('feedbackForm').reset();
    document.getElementById('wordCount').textContent = 'Words: 0 / 10 minimum';
    document.getElementById('wordCount').style.color = '#94a3b8';
    clearErrors();
    banner.style.display = 'flex'; // keep banner visible
  }, 300);
}
