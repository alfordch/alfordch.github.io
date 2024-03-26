document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("myForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "https://formspree.io/f/mjvnakyb", true);
        xhr.setRequestHeader("Accept", "application/json");

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert("Thank you! Your submission has been received.");
                // Optionally, reset the form
                document.getElementById("myForm").reset();
            }
        };

        xhr.send(formData);

    });

    document.getElementById("email").addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default form submission
            document.getElementById("myForm").submit(); // Submit the form
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("myForm2").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "https://formspree.io/f/mjvnakyb", true);
        xhr.setRequestHeader("Accept", "application/json");

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert("Thank you! Your submission has been received.");
                // Optionally, reset the form
                document.getElementById("myForm2").reset();
            }
        };

        xhr.send(formData);
        
    });

    document.getElementById("email").addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevent the default form submission
            document.getElementById("myForm2").submit(); // Submit the form
        }
    });
});