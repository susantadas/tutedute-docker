const express = require('express');
const path = require('path');
require('dotenv').config();
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


app.set('view engine', 'ejs');
const URL = process.env.BASE_URL || 'http://localhost:3001';
// dynamic import for node-fetch
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
app.use(express.static(path.join(__dirname, 'src')));
app.get('/', async function (req, res) {
    const option = { method: "GET" };
    try {
        let response = await fetch(URL + '/view', option);
        let data = await response.json();
        res.render('index', { data: data });
    } catch (e) {
        console.log(e)
        res.render('error', { data: e });
    }
});
app.get('/add', async function (req, res) {
    try {
        res.render('form');
    } catch (e) {
        console.log(e)
        res.render('error', { data: e });
    }
});
app.post('/submit', async function (req, res) {
    try {
        const option = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(req.body)
        };

        let response = await fetch(URL + '/save', option);
        console.log(response);
        if (!response.ok) {
            const text = await response.text();
            throw new Error(text);
        }

        let data = await response.json();
        console.log(data)
        res.redirect('/');
    } catch (e) {
        console.log(e);
        res.render('error', { data: e.message });
    }
});
app.listen(3000, function () {
    console.log("port number is: 3000");
});