const { GoogleAuth } = require("google-auth-library");

const auth = new GoogleAuth({
  keyFile: "keyfile.json", // your downloaded service account key
  scopes: "https://www.googleapis.com/auth/cloud-platform",
});

async function getAccessToken() {
  const client = await auth.getClient();
  const token = await client.getAccessToken();
  console.log("Access Token:", token.token);
  return token.token;
}

async function main() {
  const accessToken = await getAccessToken();
  // You can add further logic here that depends on accessToken
}

main();
