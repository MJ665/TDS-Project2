// import fs from 'fs';

// // PEM public key
// const pem =
//   "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuYcxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMIDEkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXcWyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfWed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfISI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIXdQIDAQAB";

// // Read and parse temp.json
// function readJsonFile(filePath) {
//   try {
//     const fileContent = fs.readFileSync(filePath, 'utf8');
//     const jsonData = JSON.parse(fileContent);
//     return JSON.stringify(jsonData);
//   } catch (error) {
//     console.error('Error reading or parsing temp.json:', error.message);
//     process.exit(1);
//   }
// }

// // Convert PEM to ArrayBuffer
// function pemToArrayBuffer(pem) {
//   const binary = Buffer.from(pem, 'base64');
//   return binary;
// }

// // Hash using SHA-256
// async function hash(text) {
//   const encoder = new TextEncoder();
//   const data = encoder.encode(text);
//   const hashBuffer = await crypto.subtle.digest('SHA-256', data);
//   const hashArray = Array.from(new Uint8Array(hashBuffer));
//   const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
//   return hashHex;
// }

// // Process the JSON and output the hash
// (async () => {
//   const inputData = readJsonFile('temp.json');
//   const hashResult = await hash(inputData);
//   console.log( hashResult);
// })();






import crypto from 'crypto';

// PEM public key
const pem =
  "MIIBIjANBgkqhkiG9kBAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuYcxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMIDEkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXcWyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfWed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfISI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIXdQIDAQAB";

// Hash using SHA-256
async function hash(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

// Read input data from Python using stdin
let inputData = '';
process.stdin.on('data', (chunk) => {
  inputData += chunk;
});

process.stdin.on('end', async () => {
  try {
    // Ensure valid JSON input
    const parsedJson = JSON.parse(inputData);

    // Convert to JSON string (without sorting)
    const jsonString = JSON.stringify(parsedJson, null, 0);
    
    // Generate hash
    const hashResult = await hash(jsonString);
    console.log(hashResult);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
});
