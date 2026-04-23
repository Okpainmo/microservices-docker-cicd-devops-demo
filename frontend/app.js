const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

const API_URL = process.env.API_URL || 'http://localhost:8000';
const FRONT_END_PORT = process.env.FRONT_END_PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const { title } = req.body;
    const response = await axios.post(
      `${API_URL}/jobs`,
      { title },
      { timeout: 5000 },
    );
    res.json(response.data);
  } catch (err) {
    console.error('Error submitting job:', err.message);
    res
      .status(err.response?.status || 500)
      .json({ error: err.message || 'something went wrong' });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`, {
      timeout: 5000,
    });
    res.json(response.data);
  } catch (err) {
    console.error('Error fetching job status:', err.message);
    res
      .status(err.response?.status || 500)
      .json({ error: err.message || 'something went wrong' });
  }
});

app.listen(FRONT_END_PORT, () => {
  console.log('Frontend running on port', FRONT_END_PORT);
});
