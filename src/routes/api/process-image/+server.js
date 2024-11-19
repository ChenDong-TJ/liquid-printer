import { json } from '@sveltejs/kit';
import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

// Ensure the 'saved' folder exists
const savedDir = path.join(process.cwd(), 'saved');
if (!fs.existsSync(savedDir)) {
    fs.mkdirSync(savedDir, { recursive: true });
}


export async function POST({ request }) {
    const { imageData, timestamp } = await request.json();

    // Sanitize the timestamp
    const safeTimestamp = timestamp.replace(/[^a-zA-Z0-9_-]/g, '');

    // Create the image path
    const imagePath = path.join(savedDir, `${safeTimestamp}.png`);
    console.log(`Saving image to: ${imagePath}`);

    try {
        // Save the Base64 image data as a temporary file
        try {
            fs.writeFileSync(imagePath, Buffer.from(imageData, 'base64'));
            console.log(`File successfully created at: ${imagePath}`);
        } catch (err) {
            console.error(`Error creating file: ${err.message}`);
            return json({ error: 'Failed to save image' }, { status: 500 });
        }

        // Run the Python script
        const pythonExecutable = process.env.PYTHON_EXECUTABLE || 'python';
        const pythonProcess = spawn(pythonExecutable, ['scripts/process_image.py', imagePath]);

        return await new Promise((resolve) => {
            pythonProcess.stdout.on('data', (data) => {
                console.log(`Python stdout: ${data}`);
            });

            pythonProcess.stderr.on('data', (data) => {
                console.error(`Python stderr: ${data}`);
            });

            pythonProcess.on('close', (code) => {
                // if (fs.existsSync(imagePath)) {
                //     try {
                //         fs.unlinkSync(imagePath);
                //         console.log(`File successfully deleted: ${imagePath}`);
                //     } catch (err) {
                //         console.error(`Error cleaning up file: ${err.message}`);
                //     }
                // } else {
                //     console.warn(`File not found for cleanup: ${imagePath}`);
                // }

                if (code !== 0) {
                    resolve(json({ error: 'Script execution failed' }, { status: 500 }));
                } else {
                    resolve(json({ success: true, message: 'Script executed successfully' }));
                }
            });

            pythonProcess.on('error', (err) => {
                if (fs.existsSync(imagePath)) {
                    try {
                        fs.unlinkSync(imagePath);
                    } catch (cleanupErr) {
                        console.error(`Error cleaning up file: ${cleanupErr.message}`);
                    }
                } else {
                    console.warn(`File not found for cleanup: ${imagePath}`);
                }
                resolve(json({ error: err.message }, { status: 500 }));
            });
        });
    } catch (err) {
        console.error(`Unexpected error: ${err.message}`);
        // Ensure cleanup in case of unexpected errors
        if (fs.existsSync(imagePath)) {
            try {
                fs.unlinkSync(imagePath);
            } catch (cleanupErr) {
                console.error(`Error cleaning up file: ${cleanupErr.message}`);
            }
        }
        return json({ error: 'Internal server error' }, { status: 500 });
    }
}
