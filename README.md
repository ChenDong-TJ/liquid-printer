
# Pixel Art Generator

This project is a **Pixel Art Generator**, allowing users to create pixel art, save it as a PNG file, and send it to a Python backend for processing.

---

## Features
- **Interactive Canvas**: Create pixel art using a customizable grid.
- **Save Pixel Art**: Save the artwork as a PNG file with a timestamped filename.
- **Backend Integration**: Send the artwork to a Flask backend for further processing (e.g., saving, transforming, or analyzing the image).
- **Error Handling**: Alerts users to any issues during backend communication.

---

## Installation

### Frontend: SvelteKit
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pixel-art-generator
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Access the application at `http://localhost:5173` (default SvelteKit port).

### Backend: Flask
1. Ensure you have Python 3.7+ installed.

2. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```

4. Flask will run on `http://127.0.0.1:5000`.

---

## Usage Guide

### Frontend
1. **Drawing Pixel Art**:
   - Use the interactive grid on the canvas to create your pixel art.
   - Customize the grid size and colors as desired.

2. **Save Your Artwork**:
   - Click the "Save" button to download your artwork as a PNG file. The filename will include a timestamp for uniqueness.

3. **Send to Backend**:
   - Upon saving, the application automatically sends the artwork to the backend Flask server for processing.
   - If processing is successful, a success message is logged in the browser console.

### Backend
1. The Flask server receives the image data in Base64 format.
2. The backend decodes the image and saves it in the `processed_images` directory.
3. Additional processing logic can be implemented (e.g., resizing, filters, or transformations).

---

## API Reference

### Frontend-to-Backend Communication
**Endpoint**: `/api/process-image`

**Method**: `POST`

**Request Body**:
```json
{
  "imageData": "Base64EncodedImageData",
  "timestamp": "YYYY-MM-DD-HH-MM-SS"
}
```

**Response**:
- **Success**:
  ```json
  {
    "message": "Image processed successfully",
    "path": "processed_images/pixel-art-YYYY-MM-DD-HH-MM-SS.png"
  }
  ```
- **Error**:
  ```json
  {
    "error": "Error message describing the issue"
  }
  ```

---

## Project Structure
```
pixel-art-generator/
├── src/
│   ├── routes/
│   │   ├── api/
│   │   │   └── process-image/
│   │   │       └── +server.js    # SvelteKit API for forwarding requests
│   │   └── app/                  # Frontend app files
│   └── lib/                      # Shared utility functions
├── processed_images/             # Saved images from the backend
├── app.py                        # Flask backend script
├── package.json                  # Frontend dependencies
├── README.md                     # Project documentation
└── flask_api.log                 # Optional backend log file
```

---

## Example

### Drawing Pixel Art
1. Open the canvas in your browser.
2. Draw your pixel art using the tools provided.

### Save and Send to Backend
1. Click "Save".
2. Check the `processed_images` directory in the backend for the saved image.

---

## Troubleshooting

### Common Issues
1. **Backend Not Running**:
   - Ensure the Flask server is running on `http://127.0.0.1:5000`.
   - Check for network or port conflicts.

2. **Image Not Saved**:
   - Verify the `processed_images` directory exists.
   - Check Flask logs for errors.

3. **CORS Errors**:
   - Ensure `Flask-CORS` is installed and configured in `app.py`.

---

## Future Enhancements
- Add advanced pixel art tools (e.g., symmetry, layers).
- Support for multiple file formats (e.g., JPG, SVG).
- Integrate with cloud storage for saving images.
- Real-time collaboration on pixel art projects.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

Enjoy creating stunning pixel art! 🎨
