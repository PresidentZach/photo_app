// Function to display urls fetched by url_list in views.py, and create a image_box element for each one

function displayPhotos() {

    // Somehow, we get the url_list array from views.py...
   const imagegrid = document.getElementById("grid");
   //var photourls = ??
   

// Loop through the photourls array, for each one create an image-box div 
// For now, it's just creating 5 divs
   for (let p = 0; p < 5; p++ ) {
    
    imgbox = document.createElement("div");
    imgbox.setAttribute("class", "image-box");
    //imgbox.innerHTML = '<img src= "'+ photourls.[i]+'"></img>';
    imagegrid.appendChild(imgbox);
   }

}

