document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.querySelector('input[type="file"]');

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            const fileName = this.files[0]?.name;
            const fileLabel = this.closest('label');
            let statusElement = fileLabel.querySelector(".file-status");

            if (!statusElement) {
                statusElement = document.createElement("span");
                statusElement.className = "file-status text-sm text-gray-600 ml-2";
                fileLabel.appendChild(statusElement);
            }

            statusElement.innerHTML = fileName ? `
                <span class="text-green-600">✓</span>
                Загружен файл: <span class="font-medium">${fileName}</span>
            ` : "";
        });
    }

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function () {
            document.getElementById("loading-overlay").style.display = "flex";
        });
    }
});