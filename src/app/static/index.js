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