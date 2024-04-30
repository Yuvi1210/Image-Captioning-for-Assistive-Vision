function uploadImage() {
    const fileInput = document.getElementById('uploadInput');
    const imageContainer = document.getElementById('imageContainer');
    const captionContainer = document.getElementById('captionContainer');

    const file = fileInput.files[0];
    console.log('Selected file:', file);

    const formData = new FormData();
    formData.append('file', file);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);

        // Display the uploaded image
        const imageUrl = URL.createObjectURL(file);
        console.log('Image URL:', imageUrl);
        imageContainer.innerHTML = `<img src="${imageUrl}" alt="Uploaded Image" width="300">`;
        
        // Display the generated caption
        console.log('Generated caption:', data.caption);
        captionContainer.innerHTML = `<p>${data.caption}</p>`;
    })
    .catch(error => console.error('Error:', error));
}