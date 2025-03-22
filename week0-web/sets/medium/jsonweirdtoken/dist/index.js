const jwt = require("jsonwebtoken");
const express = require("express");
const { nanoid } = require("nanoid");
const app = express();
const port = 5000;

function merge(target, source) {
  for (const attr in source) {
    if (typeof target[attr] === "object" && typeof source[attr] === "object") {
      merge(target[attr], source[attr]);
    } else {
      target[attr] = source[attr];
    }
  }
  return target;
}

const config = {
  users: {
    admin: process.env.FLAG ?? "fakeflag{zzz}",
  },
};

app.use(express.json());

app.post("/flag", (req, res) => {
  const { token } = req.body;
  if (typeof token !== "string") {
    return res.status(400).send("invalid token");
  }

  jwt.verify(config.secret ?? nanoid(16), token, (err, user) => {
    if (err) {
      return res.status(403).send("forbidden");
    } else if (user.admin !== true) {
      return res.status(401).send("unauthorized");
    }

    res.send(config.users["admin"]);
  });
});

app.post("/signup", (req, res) => {
  const user = req.body.user;
  if (typeof user !== "string" || user.indexOf("admin") > 0) {
    return res.status(400).send(":(");
  }

  try {
    const u = JSON.parse(user);
    if (typeof u !== "object") return res.status(400).send("need obj");

    merge(config.users, u);
  } catch (err) {
    console.error(err);
    return res.status(500).send("internal server error");
  }

  return res.status(200).send("OK");
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
