import express from 'express';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('static'));
app.use('/css', express.static(join(__dirname, 'static/css')));
app.use('/js', express.static(join(__dirname, 'static/js')));
app.use('/images', express.static(join(__dirname, 'static/images')));

// Routes
app.get('/', (req, res) => {
  res.sendFile(join(__dirname, 'templates/index.html'));
});

app.get('/how-it-works', (req, res) => {
  res.sendFile(join(__dirname, 'templates/how_it_works.html'));
});

app.get('/about', (req, res) => {
  res.sendFile(join(__dirname, 'templates/about.html'));
});

app.get('/contact', (req, res) => {
  res.sendFile(join(__dirname, 'templates/contact.html'));
});

app.get('/test', (req, res) => {
  res.sendFile(join(__dirname, 'templates/test.html'));
});

app.post('/api/save-results', (req, res) => {
  const results = req.body;
  res.json({
    status: 'success',
    timestamp: new Date().toISOString(),
    results: results
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});