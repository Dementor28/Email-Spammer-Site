const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.post('/send-email', upload.fields([{ name: 'imageAttachments' }, { name: 'pdfAttachments' }]), (req, res) => {
    const { senderEmail, emailPassword, receiverEmail, emailSubject, emailBody, schedule } = req.body;
    const imagePaths = (req.files.imageAttachments || []).map(file => file.path);
    const pdfPaths = (req.files.pdfAttachments || []).map(file => file.path);

    const args = [
        'email_spammer.py',
        senderEmail,
        emailPassword,
        receiverEmail,
        emailSubject,
        emailBody,
        schedule,
        ...imagePaths,
        ...pdfPaths
    ];

    const pythonProcess = spawn('python', args);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        res.sendStatus(code === 0 ? 200 : 500);
    });
});

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
