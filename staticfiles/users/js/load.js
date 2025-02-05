document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    console.log(forms);
    if (forms.length > 0) {
        forms.forEach(form => {
            form.addEventListener("submit", function () {
                document.getElementById("loading-overlay").style.display = "flex";
            });
        });
    }
});
