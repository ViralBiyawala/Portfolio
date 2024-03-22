function toggleTheme() {
    // Fetch the current theme preference from the URL
    const currentTheme = window.location.search.includes('theme_preference=dark') ? 'dark' : 'light';

    // Toggle the theme preference
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    // Redirect to the same page with the updated theme preference
    window.location.href = window.location.pathname + `?theme_preference=${newTheme}`;
}

if (document.querySelector(".pp-label")) {
    let pp = document.getElementById("profile-pic");
    let ppMain = document.getElementById("profile-pic-main");
    let pplabel = document.querySelector(".pp-label");
    let inputFile = document.getElementById("input-file");

    inputFile.onchange = function () {
        // Add AJAX here to send the image path to the server
        pp.src = URL.createObjectURL(inputFile.files[0]);
        // ppMain.src = URL.createObjectURL(inputFile.files[0]);
        const formData = new FormData();
        formData.append("image", inputFile.files[0]);

        console.log("Hi");

        fetch("/update_img/", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.text())
            .then((data) => {
                // Handle the response from the server if needed
            });
    };

    // Change Profile Photo Pencil JS
    document.addEventListener("DOMContentLoaded", function () {
        const pp = document.querySelector(".pp");
        const pplabel = pp.querySelector(".pp-label");
        var settingElement = document.getElementById('setting');

        let pp_mouse = false;

        pp.addEventListener("mouseover", function () {
            this.style.filter = "brightness(90%)";

            pplabel.style.display = "block";
            pplabel.children[0].classList.add("fa-shake");
            pplabel.children[0].style.color = "#000";
            settingElement.style.marginTop = "5rem";

            setTimeout(() => {
                if (pplabel.children[0].classList.contains("fa-shake")) {
                    pplabel.children[0].classList.remove("fa-shake");
                }
            }, 1000);
        });

        pp.addEventListener("mouseout", function () {
            this.style.filter = "brightness(100%)";
            pplabel.style.display = "none";
            settingElement.style.marginTop = "1rem";
        });
    });
}

// about_me.js
document.addEventListener('DOMContentLoaded', function () {
    // Add event listener to the "Add Blog" button
    if (document.getElementById("add-blog-btn")) {
        // Code to execute if the tag exists
        document.getElementById('add-blog-btn').addEventListener('click', function () {
            addBlogEntry();
        });

        // Function to add a new blog entry container
        function addBlogEntry() {
            // Create a new div element for the blog entry
            var blogEntry = document.createElement('div');
            blogEntry.classList.add('blog-entry');

            // Create input fields for title and content
            var titleInput = document.createElement('input');
            titleInput.setAttribute('type', 'text');
            titleInput.setAttribute('placeholder', 'Enter title');
            titleInput.classList.add('blog-title');

            var contentTextarea = document.createElement('textarea');
            contentTextarea.setAttribute('placeholder', 'Enter content');
            contentTextarea.classList.add('blog-content');

            // Create a button for updating the blog entry
            var updateBtn = document.createElement('button');
            updateBtn.textContent = 'Update';
            updateBtn.classList.add('update-btn');
            updateBtn.addEventListener('click', function () {
                updateBlogEntry(blogEntry);
            });

            // Create a button for deleting the blog entry
            // var deleteBtn = document.createElement('button');
            // deleteBtn.textContent = 'Delete';
            // deleteBtn.classList.add('delete-btn');
            // deleteBtn.addEventListener('click', function() {
            //     deleteBlogEntry(blogEntry);
            // });

            // Append input fields and buttons to the blog entry container
            blogEntry.appendChild(titleInput);
            blogEntry.appendChild(contentTextarea);
            blogEntry.appendChild(updateBtn);
            // blogEntry.appendChild(deleteBtn);

            // Append the blog entry container to the blog container
            document.getElementById('blog-container').appendChild(blogEntry);
        }

        // Function to update a blog entry
        function updateBlogEntry(blogEntry) {
            // Get title and content from the blog entry
            var title = blogEntry.querySelector('.blog-title').value;
            var content = blogEntry.querySelector('.blog-content').value;

            // Send AJAX request to update the blog entry
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/update_blog_entry/', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    // Handle success response
                    console.log('Blog entry updated successfully');
                }
            };
            var data = JSON.stringify({ 'title': title, 'content': content });
            xhr.send(data);
        }
    }
});

// Function to handle delete button click
document.querySelectorAll('.delete-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
        // Get title and content from data attributes
        var title = this.getAttribute('data-title');
        var content = this.getAttribute('data-content');

        // Send AJAX request to delete the blog entry
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/delete_blog_entry/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // Handle success response
                    console.log('Blog entry deleted successfully');
                    // Remove the blog entry from the DOM
                    btn.closest('.blog-entry').remove();
                    window.location.reload();

                } else {
                    // Handle error response
                    console.error('Failed to delete blog entry');
                }
            }
        };
        var data = JSON.stringify({ 'title': title, 'content': content });
        xhr.send(data);
    });
});

// dashboard.js
if (document.getElementById("add-education-form")) {
    // Function to handle submission of the add education form
    document.getElementById('add-education-form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = new FormData(this);

        // Send AJAX request to add new education entry
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/add_education_entry/', true);
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}'); // Set CSRF token
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Handle success response
                console.log('New education entry added successfully');
                // Reload the page to reflect changes
                window.location.reload();
            }
        };
        xhr.send(formData);
    });

    // Function to handle click event on the "Add Education" button
    document.getElementById('add-education-btn').addEventListener('click', function () {
        // Toggle visibility of the add education form
        var addEducationForm = document.getElementById('add-education-form');
        addEducationForm.style.display = addEducationForm.style.display === 'none' ? 'block' : 'none';
    });
}

// dashboard.js
if (document.getElementById("add-skill")) {
    // Function to handle submission of the add education form
    document.getElementById('add-skill').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Get form data
        var formData = new FormData(this);

        // Send AJAX request to add new education entry
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/add_skill/', true);
        xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}'); // Set CSRF token
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // Handle success response
                console.log('New Skill added successfully');
                // Reload the page to reflect changes
                window.location.reload();
            }
        };
        xhr.send(formData);
    });

    var deleteButtons = document.querySelectorAll('.delete-skill-btn');
    deleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var skillName = this.getAttribute('data-skill');
            var formData = new FormData();
            formData.append('skill', skillName);
            formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/del_skill/', true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    location.reload();  // Refresh the page after deleting skill
                }
            };
            xhr.send(formData);
        });
    });

}

// dashboard.js
if (document.getElementById("add-certificate")) {
    var addCertificateBtn = document.getElementById('add-certificate');
    addCertificateBtn.addEventListener('click', function () {
        var certificateFormContainer = document.getElementById('certificate-form-container');
        certificateFormContainer.style.display = (certificateFormContainer.style.display === 'none') ? 'block' : 'none';
    });

    var certificateForm = document.getElementById('certificate-form');
    certificateForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(certificateForm);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/add_certificate/', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                location.reload(); // Reload the page after successfully adding certificate
            }
            else {
                console.log("Failed to add certificate");
            }
        };
        xhr.send(formData);
    });


    document.querySelectorAll('.edit-certificate-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var certificateId = this.getAttribute('data-certificate-id');
            var editForm = document.getElementById('edit_form_' + certificateId);
            editForm.style.display = (editForm.style.display === 'none') ? 'block' : 'none';
        });
    });

    document.querySelectorAll('.save-edit-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var certificateId = this.getAttribute('data-certificate-id');
            var issuedBy = document.getElementById('edit_issued_by_' + certificateId).value;
            var linkBy = document.getElementById('edit_link_by_' + certificateId).value;
            var titleBy = document.getElementById('edit_title_by_' + certificateId).value;
            var expiryDate = document.getElementById('edit_expiry_date_' + certificateId).value;
            var dateAwarded = document.getElementById('edit_date_awarded_' + certificateId).value;
            var skillsGained = document.getElementById('edit_skills_gained_' + certificateId).value;
            var displayOrder = document.getElementById('edit_display_order_' + certificateId).value;
            var image = document.getElementById('edit_image_' + certificateId).files[0];

            var formData = new FormData();
            formData.append('issued_by', issuedBy);
            formData.append('link', linkBy);
            formData.append('title', titleBy);
            formData.append('date_awarded', dateAwarded);
            formData.append('expiry_date', expiryDate);
            formData.append('skills_gained', skillsGained);
            formData.append('display_order', displayOrder);
            formData.append('image', image);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/update_certificate/' + certificateId + '/', true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        location.reload();
                    } else {
                        // Handle errors if update fails
                        console.error('Error updating certificate:', response.errors);
                    }
                }
            };
            xhr.send(formData);
        });
    });
}

// dashboard.js
if (document.getElementById("add-project")) {
    var addCertificateBtn = document.getElementById('add-project');
    addCertificateBtn.addEventListener('click', function () {
        var certificateFormContainer = document.getElementById('project-form-container');
        certificateFormContainer.style.display = (certificateFormContainer.style.display === 'none') ? 'block' : 'none';
    });

    var certificateForm = document.getElementById('project-form');
    certificateForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(certificateForm);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/add_project/', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                location.reload(); // Reload the page after successfully adding certificate
            }
            else {
                console.log("Failed to add Project");
            }
        };
        xhr.send(formData);
    });

    document.querySelectorAll('.edit-project-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var projectId = this.getAttribute('data-project-id');
            var editForm = document.getElementById('edit_form_' + projectId);
            editForm.style.display = (editForm.style.display === 'none') ? 'block' : 'none';
        });
    });

    document.querySelectorAll('.save-edit-btn-pr').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var projectId = this.getAttribute('data-project-id');
            var titleBy = document.getElementById('edit_title_by_' + projectId).value;
            var image = document.getElementById('edit_image_' + projectId).files[0];
            var description = document.getElementById('edit_description_' + projectId).value;
            var projectType = document.getElementById('edit_project_type_' + projectId).value;
            var codelinkBy = document.getElementById('edit_code_link_' + projectId).value;
            var codeType = document.getElementById('edit_code_type_' + projectId).value;
            var livelinkBy = document.getElementById('edit_live_link_' + projectId).value;
            var displayOrder = document.getElementById('edit_display_order_' + projectId).value;

            var formData = new FormData();
            formData.append('title', titleBy);
            formData.append('image', image);
            formData.append('description', description);
            formData.append('project_type', projectType);
            formData.append('code_link', codelinkBy);
            formData.append('code_type', codeType);
            formData.append('live_link', livelinkBy);
            formData.append('display_order', displayOrder);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/update_project/' + projectId + '/', true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        location.reload();
                    } else {
                        // Handle errors if update fails
                        console.error('Error updating certificate:', response.errors);
                    }
                }
            };
            xhr.send(formData);
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const groups = document.querySelectorAll('.project-group');
    groups.forEach(group => {
        group.addEventListener('click', function () {
            const groupId = this.getAttribute('data-group');
            const projects = document.querySelectorAll('.projects');
            projects.forEach(project => {
                if (project.id === groupId) {
                    project.classList.toggle('visi');
                } else {
                    project.classList.remove('visi');
                }
            });
        });
    });
});