const fs = require('fs');
const path = require('path');

// Search web/ directory for multipart/form-data
const webDir = 'd:\\WeKnora\\web\\assets';
const files = fs.readdirSync(webDir);
const mainBundle = files.find(f => f.startsWith('index-') && f.endsWith('.js'));
const content = fs.readFileSync(path.join(webDir, mainBundle), 'utf-8');

// More thorough search
const idx = content.indexOf('multipart/form-data');
if (idx >= 0) {
  console.log('Found multipart/form-data at index', idx);
  console.log('Context:', content.slice(Math.max(0, idx - 100), idx + 100));
} else {
  console.log('multipart/form-data NOT found in web bundle');
}

// Search for postUpload
const idx2 = content.indexOf('postUpload');
if (idx2 >= 0) {
  console.log('\nFound postUpload at index', idx2);
  console.log('Context:', content.slice(Math.max(0, idx2 - 50), idx2 + 300));
} else {
  console.log('postUpload NOT found');
}

// Search for the specific fix pattern - just X-Request-ID without Content-Type
const idx3 = content.indexOf('X-Request-ID');
if (idx3 >= 0) {
  console.log('\nFound X-Request-ID at index', idx3);
  console.log('Context:', content.slice(Math.max(0, idx3 - 100), idx3 + 100));
}

// Compare with production
console.log('\n=== Production check ===');
const https = require('https');
function req(options) {
  return new Promise((res, rej) => {
    const r = https.request(options, x => {
      let b = '';
      x.on('data', c => b += c);
      x.on('end', () => res({ code: x.statusCode, body: b }));
    });
    r.on('error', rej);
    r.end();
  });
}

(async () => {
  let prod = await req({ hostname: 'wiki258.zeabur.app', path: '/assets/index-BHwvPCGc.js', method: 'GET' });
  console.log('Prod bundle size:', prod.body.length);
  console.log('Prod has multipart/form-data:', prod.body.includes('multipart/form-data'));
  const pidx = prod.body.indexOf('postUpload');
  if (pidx >= 0) {
    console.log('Prod postUpload context:', prod.body.slice(Math.max(0, pidx - 50), pidx + 300));
  }
})();
