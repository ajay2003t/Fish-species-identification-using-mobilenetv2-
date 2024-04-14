document.getElementById('imageInput').addEventListener('change', function () {
    var reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById('uploadedImage').src = e.target.result;
    };
    reader.readAsDataURL(this.files[0]);
});

function predict() {
    var input = document.getElementById('imageInput');
    var file = input.files[0];

    if (file) {
        var formData = new FormData();
        formData.append('file', file);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            displayResult(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Please select an image.');
    }
}

function displayResult(result) {
    var resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `Predicted class: ${result.class_label}<br>Confidence: ${result.confidence.toFixed(2)}`;

    // You can use result.class_label and result.confidence for further processing or display.
}
