
  // Sidebar click triggers hidden file input
    document.getElementById('sidebar-upload').addEventListener('click', function () {
        document.getElementById('hidden-upload').click();
  });

    // Drag-and-drop functionality
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("photoUpload");

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => {
            e.preventDefault();
            e.stopPropagation();
        }, false);
  });

  dropArea.addEventListener('dragover', () => {
        dropArea.classList.add('dragging');
  });

  dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragging');
  });

  dropArea.addEventListener('drop', e => {
        dropArea.classList.remove('dragging');
    fileInput.files = e.dataTransfer.files;
    document.getElementById("upload-form").submit();
  });

  //logic for search bar stuff
document.getElementById('search-bar').addEventListener('input', function () {
    const query = this.value.toLowerCase();
    const photos = document.querySelectorAll('.image-box');

    photos.forEach(photo => {
        const infoId = `${photo.id}_info`;
        const info = document.getElementById(infoId);
        if (!info) return;

        const infoParts = info.innerHTML.split(';');
        const tags = infoParts[2].toLowerCase(); // index 2 = tags
        const match = tags.includes(query);

        photo.style.display = match || query === "" ? "block" : "none";
    });
});
