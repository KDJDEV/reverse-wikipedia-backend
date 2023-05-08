import express from "express";
import fileUpload from "express-fileupload";
import fetch from 'node-fetch';
import cors from 'cors';
import https from 'https';
import fs from 'fs';
const app = express();
const privateKey = fs.readFileSync('/root/.acme.sh/api.reversewikipedia.com/api.reversewikipedia.com.key', 'utf8');
const certificate = fs.readFileSync('/root/.acme.sh/api.reversewikipedia.com/api.reversewikipedia.com.cer', 'utf8');
const ca = fs.readFileSync('/root/.acme.sh/api.reversewikipedia.com/fullchain.cer', 'utf8');
const credentials = {
	key: privateKey,
	cert: certificate,
	ca: ca
};
var corsOptions = {
    origin: 'https://www.reversewikipedia.com',
    optionsSuccessStatus: 200 // some legacy browsers (IE11, various SmartTVs) choke on 204
}
app.use(cors(corsOptions))
app.use(fileUpload());
app.use(express.json());
app.use(express.static('public'));

const allowedContentTypes = ["image/avif", "image/bmp", "image/gif", "image/vnd.microsoft.icon", "image/jpeg", "image/png", "image/svg+xml", "image/tiff", "image/webp"];
function contentTypeAllowed(typeString) {
    for (const type of allowedContentTypes) {
        if (typeString.indexOf(type) !== -1) {
            return true;
        }
    }
    return false;
}
app.get('/getImageFromUrl/:url', async (req, res) => {
    try {
        let url = req.params.url;
        if (url.indexOf("http") === -1) {
            url = "https://" + url;
        }
        let img = await fetch(url);
        const contentType = img.headers.get("content-type");
        if (!contentTypeAllowed(contentType)) {
            res.writeHead(400, {
                'Content-Type': contentType
            });
            res.end("error code: 2");
            return;
        }
        let imgBuffer = Buffer.from(await img.arrayBuffer());
        res.writeHead(200, {
            'Content-Type': contentType
        });
        res.end(imgBuffer);
    } catch (e) {
        res.status(400).send("error code: 1");
    }
});
app.post('/upload', async (req, res) => {
    
    const resp = await fetch(`http://127.0.0.1:8080?page=${req.query.page}`, { method: "POST", body: req.files.image.data });
    if (resp.status === 200) {
        res.json(await resp.json());
    } else {
        res.sendStatus(400);
    }
});

app.post('/submitForm', async (req, res) => {
    try {
        const body = req.body;
        Object.keys(body).forEach(function (key) {
            if (body[key] === "") body[key] = "Not provided";
        });
        const data = {
            "content": "@everyone Received message from form",
            "embeds": [
                {
                    "title": 'Information:',
                    "description": `First name: ${body.first_name}\n Last name: ${body.last_name}\nEmail: ${body.email}\nCompany Name: ${body.company_name}\n`
                },
                {
                    "title": 'Message:',
                    "description": body.message
                }
            ]
        }

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        };

        const webhookResponse = await fetch("https://discord.com/api/webhooks/1061075483049078814/76l21d5cZ94SrrcG2M11z3A_s_vdL3Nn4LeJgPq8JIVHRHagiZ8uYku89W1Umf3IU80k", options);
        if (webhookResponse.status !== 204) {
            throw new Error(`the status code (${webhookResponse.status}) of the webhook request denotes an error`);
        }
        res.sendStatus(200);
    } catch (e) {
        console.log(e);
        res.sendStatus(500);
    }
})
const httpsServer = https.createServer(credentials, app);
httpsServer.listen(443, () => {
	console.log('HTTPS Server running on port 443');
});

app.listen(80, () => {
  console.log(`HTTP Server running on port 80`)
})
