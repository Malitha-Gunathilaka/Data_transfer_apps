from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mkv', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'zip', 'rar'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DataSwift Pro</title> <!-- Updated title here -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-..." crossorigin="anonymous" referrerpolicy="no-referrer" />
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
            }
            form {
                margin: 20px 0;
            }
            input[type="file"] {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type="submit"] {
                padding: 10px 20px;
                border: none;
                background-color: #28a745;
                color: #fff;
                border-radius: 4px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #218838;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
            }
            .delete-btn {
                color: #dc3545;
                cursor: pointer;
                margin-left: 10px;
            }
            .delete-btn:hover {
                text-decoration: underline;
            }
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #333;
                color: white;
                text-align: center;
                padding: 10px 0;
            }
            .footer a {
                color: white;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>DataSwift Pro</h1> <!-- Updated heading here -->
            <h2>Upload new file(s)</h2>
            <form action="/upload" method="post" enctype="multipart/form-data" onsubmit="return validateForm()">
                <input type="file" name="file" multiple>
                <input type="submit" value="Upload">
            </form>
            <h2>Available Files</h2>
            <ul>
                {% for file in files %}
                <li>
                    <a href="{{ url_for('uploaded_file', filename=file) }}">{{ file }}</a>
                    <span class="delete-btn" onclick="deleteFile('{{ file }}')"><i class="fas fa-trash-alt"></i></span>
                </li>
                {% endfor %}
            </ul>
        </div>
        <div class="footer">
            <p>Developed by <a href="mailto:malithavisada@gmail.com">Malitha Visada</a> &nbsp&nbsp <a href="https://linkedin.com/in/malithavisada" target="_blank"><i class="fab fa-linkedin"></i></a> &nbsp <a href="https://github.com/Malitha-Gunathilaka" target="_blank"><i class="fab fa-github"></i></a></p>
        </div>
        <script>
            function validateForm() {
                var fileInput = document.querySelector('input[type="file"]');
                if (fileInput.files.length === 0) {
                    alert("Please select at least one file to upload.");
                    return false;
                }
                return true;
            }
            
            function deleteFile(filename) {
                if (confirm("Are you sure you want to delete " + filename + "?")) {
                    fetch('/delete/' + filename, {
                        method: 'DELETE',
                    })
                    .then(response => {
                        if (response.ok) {
                            window.location.reload();
                        } else {
                            alert('Failed to delete ' + filename);
                        }
                    })
                    .catch(error => {
                        console.error('Error deleting file:', error);
                        alert('Error deleting ' + filename);
                    });
                }
            }
        </script>
    </body>
    </html>
    ''', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part. Please choose a file.', 400
    files = request.files.getlist('file')
    for file in files:
        if file.filename == '':
            return 'No selected file. Please choose a file.', 400
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        os.remove(file_path)
        return '', 204  # Return no content on successful deletion
    except Exception as e:
        print(f"Error deleting file {filename}: {str(e)}")
        return '', 500  # Return server error if deletion fails

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
