document.querySelectorAll("form[id^='reservation-form']").forEach(form => {
    const csrftoken = getCookie('csrftoken');
    
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        fetch(form.action || "", {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": csrftoken,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({ icon: "success", title: "Reservation Successful!", html: data.message });
                form.reset();
            } else {
                Swal.fire({ icon: "error", title: "Fix errors", html: Object.values(data.errors).join("<br>") });
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
            Swal.fire({ icon: "error", title: "Error!", text: "Something went wrong. Please try again later." });
        });
    });
});
