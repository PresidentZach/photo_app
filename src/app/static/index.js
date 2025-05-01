// Function to display urls fetched by url_list in views.py, and create a image_box element for each one

function displayPhotos() {

    // Somehow, we get the url_list array from views.py...
    var photourls = {{ url_list_json }};
   const imagegrid = document.getElementById("grid");
   
   

// Loop through the photourls array, for each one create an image-box div 

   for (let p = 0; p < photourls.length; p++ ) {
    
    imgbox = document.createElement("div");
    imgbox.setAttribute("class", "image-box");
    //imgbox.innerHTML = "<p>"+ photourls +"</p>";
    imagegrid.appendChild(imgbox);
   }

}

