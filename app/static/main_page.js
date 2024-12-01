import JSZip from "jszip";

document.addEventListener('DOMContentLoaded', () => {
    // Containers
    const dataContainer = document.getElementById('dataContainer');
    const imageContainer = document.getElementById('imageContainer');
    // Drop-down
    const pollenDropdown = document.getElementById('pollen_name');
    // Buttons
    const fetchDataBtn = document.getElementById('fetchDataBtn');
    const fetchJoinDataBtn = document.getElementById('joinDataBtn');
    const createZipBtn = document.getElementById('createZipBtn')
    const downloadZipBtn = document.getElementById('downloadZipBtn');
    const fetchAnnotationsBtn = document.getElementById('fetchAnnotationsBtn');
    const displayImagesBtn = document.getElementById('displayImagesBtn'); // image display
    const selectDeselectAllBtn = document.getElementById('selectDeselect'); // select/deselect all images button (new)
    const imageToZipBtn = document.getElementById('imageToZipBtn');
    // Global variable
    let displayedData = null;
    
    // Hide download zip button
    downloadZipBtn.style.display = 'none';
    
    // Displays download button after there's data in both containers 
    function checkDataAndImageContainer(dataContainer, imageContainer){
        if (dataContainer.innerHTML.trim() !== '' && imageContainer.innerHTML.trim() !== ''){
            downloadZipBtn.style.display = 'inline-block'; // Makes the download zip button reappear
        }
    }

    // Table structure for all data being fetched (REUSED)
    function generateTableHTML(data){
        const selectedPollen = pollenDropdown.value.charAt(0).toUpperCase() + 
            pollenDropdown.value.slice(1); // Capitalizes the first letter of pollen name

        return `<h2>Query Results For ${selectedPollen}</h2><table><thead><tr>` + 
                Object.keys(data[0]).map(key => `<th>${key}</th>`).join('') + 
                '</tr></thead><tbody>' + data.map(row => '<tr>' + 
                Object.values(row).map(item => `<td>${item}</td>`).join('') + 
                '</tr>').join('') + '</tbody></table>';
    }
    
    // Requests for DB data
    async function fetchData(endpoint, selectedPollen) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ pollen_name: selectedPollen }),
            });
            // Checks if there's a backend connection 
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            // If request is successful, response.json() parses the JSON from server and returns JS object
            const data = await response.json(); 
            return data;

        } catch (error) {
            console.error('Fetch error:', error);
            return null;
        }
    }
    
    // Requests for images
    async function fetchImages(endpoint, selectedPollen) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST', // This means that the request should use the POST method (Sends data to server)
                headers: { 'Content-Type': 'application/json' }, // Informs server that the request contains JSON data
                body: JSON.stringify({ pollen_name: selectedPollen }) // Send as JSON
            });

            if (!response.ok) throw new Error(`Error fetching images: ${response.statusText}`);

            // Get image paths from response
            const imagePaths = await response.json();
            
            // console.log for testing purposes
            console.log(`This is the imagePaths array: ${imagePaths}`)

            // Ensure the response is an array of strings (paths)
            if (Array.isArray(imagePaths)) {
                return imagePaths;
            } else {
                throw new Error('Response is not in expected format (array of image paths)');
            }

        } catch (error) {
            console.error('Image Fetch error:', error);
            throw error;
        }
    }

    // Ensures data retrieved is valid and displays data in tabular form
    async function handleFetchData(event, endpoint) {
        event.preventDefault();
        const selectedPollen = pollenDropdown.value;
        const data = await fetchData(endpoint, selectedPollen);
        
        if (data && data.length > 0) {
            displayedData = data // sets the fetched data to a global variable which will be used later
            dataContainer.innerHTML = generateTableHTML(data);
        } else {
            dataContainer.innerHTML = '<h1>No results found</h1>';
        }
        
        // Check if both containers are populated to display downloadZipBtn button
        checkDataAndImageContainer(dataContainer, imageContainer);
    }

    // Ensures Images retrieved is valid and displays images  
    async function handleFetchImages(event, endpoint) {
        event.preventDefault();
        const selectedPollen = pollenDropdown.value;
        const imagePaths = await fetchImages(endpoint, selectedPollen);

        try {
            // Clear any existing images
            imageContainer.innerHTML = ''; 

            // Create img elements for each image path and append them to the imageContainer
            if (Array.isArray(imagePaths) && imagePaths.length > 0) {
                
                // Loops through array, assigns path for each to the src, and adds to the container
                imagePaths.forEach((path, index) => {
                    const imgElement = document.createElement('img');
                    imgElement.src = path; // The path returned by the server
                    imgElement.alt = `Pollen Image ${index + 1}`; // Returns a text description if image not available
                    
                    // Add click event to toggle selection
                    imgElement.addEventListener('click', () => {
                        imgElement.classList.toggle('selected'); // Toggles between select/deselect
                    })
                    
                    // Append all changes made to each image to the image container
                    imageContainer.appendChild(imgElement);
                });
            } else {
                imageContainer.innerHTML = "<p>No images found for the selected pollen.</p>";
            }
        } catch (error) {
            // In case of error, show a user-friendly message
            imageContainer.innerHTML = "<p>Failed to load images. Please try again.</p>";
        }
        // Check if both containers are populated to display downloadZipBtn button
        checkDataAndImageContainer(dataContainer, imageContainer);
    }

    // Checks if images are all selected, then deselect them. If all are deselected, then select them
    function toggleSelectAll() {
        const allImages = document.querySelectorAll('#imageContainer img'); // Get all images
        const areAllSelected = Array.from(allImages).every(img => img.classList.contains('selected')); // Check if all are selected

        // if all images are selected, deselect all, otherwise, select all
        allImages.forEach(img => {
            if (areAllSelected) {
                img.classList.remove('selected') // Deselect all images
            } else {
                img.classList.add('selected'); // Select all images
            }
        });

    }

    // might have to re do the below function.
    // name it convertToBlob and have it handle both tabular data and image data.
    // right now i am just turning image data into blob, not knowing that tabular 
    // data needs to be turned into blob format as well
    // UPDATE: I have decided to create two separate functions to deal with each data type (image data, tabular data)

    // Stores user selected images (FOR ZIP DOWNLOAD FUNCTIONALITY)
    async function imageToBlob() {
        const selectedImages = document.querySelectorAll('#imageContainer img.selected');
        const blobs = [] // declare variables with either let or const, do not forget

        // include error handling in here

        for (const img of selectedImages) {
            const blob = await fetch (img.src).then( res => res.blob() );
            blobs.push(blob);
        }

        console.log(blobs.length);
        return blobs;
    
    }

    async function annotationDataToBlob() {

    }


    async function handleDataDownload() {
        const selectedAnnotationData = annotationData; // Contains the fetched data (NON-Blob)
        const imageData = getSelectedImages(); // Contains images in blob format
        const zip = new JSZip();

        if (imageData.length !== 0 && selectedAnnotationData !== 0) {
            // Add image to ZIP file

            // Add annotation data


            // Generate the ZIP file and trigger the download
        }


    }

    // Event listeners using the reusable function above
    fetchDataBtn.addEventListener('click', (event) => handleFetchData(event, endpoints.fetchData));
    fetchJoinDataBtn.addEventListener('click', (event) => handleFetchData(event, endpoints.getRelatedDataJoin));
    fetchAnnotationsBtn.addEventListener('click', (event) => handleFetchData(event, endpoints.getAnnotations));
    displayImagesBtn.addEventListener('click', (event) => handleFetchImages(event, endpoints.fetchImages));
    selectDeselectAllBtn.addEventListener('click', toggleSelectAll);
    // imageToZipBtn.addEventListener('click', getSelectedImages); created this for testing purposes, can be discarded
});

// IMPROVEMENTS FROM CHATGPT
// Additional Considerations:
// Debounce Button Clicks: If the buttons (fetchDataBtn, fetchJoinDataBtn, etc.) are pressed multiple times quickly, it might lead to unnecessary fetch requests. Consider debouncing the button clicks to avoid redundant calls.
// Learn more about Debouncing
// CSS Styling for Selected State: Ensure you have styles defined for the .selected class so that users can clearly see which images are selected. You could use styles like a border, opacity change, or background color to highlight selected images.