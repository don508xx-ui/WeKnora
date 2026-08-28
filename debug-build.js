const https = require('https');

function req(options, body) {
  return new Promise((res, rej) => {
    const r = https.request(options, x => {
      let b = '';
      x.on('data', c => b += c);
      x.on('end', () => res({ code: x.statusCode, body: b, headers: x.headers }));
    });
    r.on('error', rej);
    if (body) r.write(body);
    r.end();
  });
}

(async () => {
  // Check if latest commit is deployed by checking frontend dist for the fix
  let index = await req({ hostname: 'wiki258.zeabur.app', path: '/index.html', method: 'GET' });
  console.log('Index:', index.code);
  
  // Check the request.ts fix by looking at the JS bundle
  // The fix removes Content-Type from postUpload - let's check if the old version is cached
  let hasBoundaryFix = await req({ hostname: 'wiki258.zeabur.app', path: '/assets/index-BHwvPCGc.js', method: 'GET' });
  console.log('JS bundle:', hasBoundaryFix.code, 'size:', hasBoundaryFix.body.length);
  
  // Check if the old Content-Type code is still in the bundle
  const hasOldUploadCode = hasBoundaryFix.body.includes('multipart/form-data');
  console.log('Has old multipart/form-data hardcode:', hasOldUploadCode);
  
  // The fix removed the hardcoded Content-Type from postUpload
  // Old code: "Content-Type", "multipart/form-data"
  // New code: only has "X-Request-ID"
  const hasNewPostUpload = hasBoundaryFix.body.includes('X-Request-ID') && !hasBoundaryFix.body.includes('"Content-Type":"multipart/form-data"');
  console.log('Has new postUpload (no hardcoded CT):', hasNewPostUpload);

  // Now check the Vue error - search for the 'in' operator issue
  // Look for 'key' usage in iterables
  const hasKeyInOperator = hasBoundaryFix.body.includes('"key"') || hasBoundaryFix.body.includes("'key'");
  console.log('Has key string:', hasKeyInOperator);
  
  // Check if the /files bypass is in the backend
  // Test /files directly
  let l = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/auth/login', method: 'POST', headers: { 'Content-Type': 'application/json' } }, JSON.stringify({ email: '28451613@qq.com', password: 'qzt360' }));
  let tok = JSON.parse(l.body).token;
  let H = { Authorization: 'Bearer ' + tok };
  
  let filesTest = await req({ hostname: 'wiki258.zeabur.app', path: '/files?file_path=local://10000/779dc39b-eb42-4d50-83af-a1bd180c3aaf/1787904425861932893.pdf', method: 'GET', headers: H });
  console.log('\n/files endpoint:', filesTest.code, 'content-type:', filesTest.headers['content-type']);
  console.log('Is PDF:', filesTest.headers['content-type']?.includes('pdf'));
})();
