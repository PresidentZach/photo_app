// Function to display urls fetched by url_list in views.py, and create a image_box element for each one

function displayPhoto() {

    var photourls = "{{url_list}}";
    var imagegrid = document.getElementByClassName("image-grid");


// Loop through the photourls array, for each one create an image-box div 

    for (let p = 0; p < photourls.length; p++ ) {
        imgbox = document.createElement("div");
        imgbox.setAttribute("class", "image-box");
        // create an img thumbnail inside with the src attribute of the current list item
        div.innerHTML = '<img class="thumb" src="'+ photourls[i]+ '"/></img>';
        // add this div to image-grid
        imagegrid.appendChild(imagegrid);
    }

}

// test function (remove later)
function testFn() {
    document.getElementById("test").innerHTML = "test worked!";
}

<script>
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
</script>
