// main.js
const config = require('./config.js');
const axios = require('axios'); // Install: npm install axios

const targetPhone = '08123456789';

async function sendOTP(platform) {
  // Format nomor sesuai kebutuhan platform
  const formattedPhone = config.generateRandom.phone(platform.phoneFormat, targetPhone);
  
  // Ganti placeholder di body
  let body = JSON.stringify(platform.body);
  body = body.replace(/{phone_08}/g, formattedPhone)
             .replace(/{phone_62}/g, formattedPhone)
             .replace(/{phone_plus}/g, formattedPhone)
             .replace(/{phone_nocode}/g, formattedPhone)
             .replace(/{phone_int}/g, formattedPhone)
             .replace(/{random_name}/g, config.generateRandom.name())
             .replace(/{random_email}/g, config.generateRandom.email())
             .replace(/{random_password}/g, config.generateRandom.password())
             .replace(/{uuid}/g, config.generateRandom.uuid());

  try {
    const response = await axios({
      method: platform.method,
      url: platform.url,
      headers: platform.headers,
      data: JSON.parse(body),
      timeout: 10000
    });
    console.log(`✅ ${platform.name}: ${response.status}`);
  } catch (error) {
    console.log(`❌ ${platform.name}: ${error.message}`);
  }
}

// Jalankan semua platform
async function runAll() {
  for (const platform of config.platforms) {
    await sendOTP(platform);
    // Delay antar request agar tidak kena rate limit
    await new Promise(resolve => setTimeout(resolve, 500));
  }
}

runAll();