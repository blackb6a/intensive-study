const jwt = require("jsonwebtoken");
const express = require("express");
const { nanoid } = require("nanoid");
const app = express();
const port = 5000;

const FLAG = process.env.FLAG ?? "fakeflag{zzz}";
let secret = null;

try {
  secret = nanoid(-1337);
} catch {
  /**/
}

app.use(express.json());

app.post("/flag", (req, res) => {
  const { token } = req.body;
  if (typeof token !== "string") {
    return res.status(400).send("invalid token");
  }

  jwt.verify(token, secret, (err, user) => {
    if (err) {
      return res.status(403).send("forbidden");
    } else if (user.admin !== true) {
      return res.status(401).send("unauthorized");
    }

    res.send(FLAG);
  });
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
