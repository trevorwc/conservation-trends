const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Route for the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route for trends in science
app.get('/trends-science', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'trends_science.html'));
});

// Route for trends in policy
app.get('/trends-policy', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'trends_policy.html'));
});

// Route for comparison page
app.get('/comparison', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'comparison.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});