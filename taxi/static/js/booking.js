const steps = Array.from(document.querySelectorAll('.step'));
const nextBtns = document.querySelectorAll('.next-btn');
const prevBtns = document.querySelectorAll('.prev-btn');
const form = document.getElementById('reservation-form');  // <-- updated here

let currentStep = 0;

nextBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        if (currentStep < steps.length - 1) {
            steps[currentStep].classList.remove('active');
            currentStep++;
            steps[currentStep].classList.add('active');
        }
        if (currentStep === steps.length - 1) {
            showReview();
        }
    });
});

prevBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        if (currentStep > 0) {
            steps[currentStep].classList.remove('active');
            currentStep--;
            steps[currentStep].classList.add('active');
        }
    });
});

function showReview() {
    const review = document.getElementById('review-details');
    const formData = new FormData(form);
    let output = '';
    for (const [key, value] of formData.entries()) {
        output += `<p><strong>${key.replace(/_/g, ' ')}:</strong> ${value}</p>`;
    }
    review.innerHTML = output;
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Booking submitted!');
    form.reset();
    steps[currentStep].classList.remove('active');
    currentStep = 0;
    steps[currentStep].classList.add('active');
});
