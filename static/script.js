document.addEventListener("DOMContentLoaded", () => {
            const button = document.querySelector("[data-download]");
            const img = document.getElementById("gridImg");

            button.addEventListener("click", () => {
                const a = document.createElement("a");
                a.href = img.src;
                a.download = "downloaded_image.jpg";
                a.style.display = "none";

                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
        });