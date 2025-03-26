const fs = require("fs");
const { v4: uuidv4 } = require("uuid");
const axios = require("axios");

let key = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"; // Azure Translator API subscription key
let endpoint = "https://ai-aihackthonhub282549186415.cognitiveservices.azure.com"; // Azure Translator API endpoint
let region = "global"; // Azure region

// Function to translate text into multiple languages using Azure Translator API
async function translateText(
  sampleText, // Text to be translated
  targetLanguages // Array of target language codes
) {
  try {
    // Make POST request to Azure Translator API
    const response = await axios.post(
      `${endpoint}/translate?api-version=3.0&to=${targetLanguages}`,
      [{ text: sampleText }],
      {
        // Request headers
        headers: {
          "Ocp-Apim-Subscription-Key": key, // Subscription key
          "Ocp-Apim-Subscription-Region": region, // Azure region
          "Content-type": "application/json",
          "X-ClientTraceId": uuidv4().toString(), // Client trace ID
        },
      }
    );

    console.log(response.data); // Log the response data
    console.log(response.data[0].translations); // Log the translations
    console.log(response.data[0].detectedLanguage); // Log the detected language

    // optional: Write output to a JSON file
    fs.writeFileSync("output.json", JSON.stringify(response.data));
  } catch (error) {
    console.log(error); // Log the error
  }
}

// Array of target language codes
let targetLanguageCodes = ["af", "sq", "am", "ur", "he", "en", "prs"];

// Call translateText function with sample text and target language codes
translateText(
  "My name is Johar and I am a software developer", // Sample text
  targetLanguageCodes // Target language codes
);

// URL to get supported languages
// https://api.cognitive.microsofttranslator.com/languages?api-version=3.0