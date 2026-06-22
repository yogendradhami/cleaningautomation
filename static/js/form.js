// Simple client-side validation for the contact form
document.addEventListener('DOMContentLoaded', function () {
  var form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    var name = form.querySelector('input[name="name"]').value.trim();
    var email = form.querySelector('input[name="email"]').value.trim();
    var message = form.querySelector('textarea[name="message"]').value.trim();
    var honeypot = form.querySelector('input[name="phone"]').value.trim();

    if (honeypot) {
      // Filled honeypot — likely spam: prevent submission
      e.preventDefault();
      return false;
    }

    if (!name || !email || !message) {
      e.preventDefault();
      alert('Please complete all required fields.');
      return false;
    }

    // Basic email format check
    var re = /^\S+@\S+\.\S+$/;
    if (!re.test(email)) {
      e.preventDefault();
      alert('Please enter a valid email address.');
      return false;
    }

    // allow submit
    return true;
  });
});
