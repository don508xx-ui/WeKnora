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
  let l = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/auth/login', method: 'POST', headers: { 'Content-Type': 'application/json' } }, JSON.stringify({ email: '28451613@qq.com', password: 'qzt360' }));
  let tok = JSON.parse(l.body).token;
  let H = { Authorization: 'Bearer ' + tok };

  // 1. List ALL knowledge - show IDs and file status
  let k = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/knowledge-bases/4b1c1c0a-64d4-4d3b-b605-0f984e66b7c8/knowledge?page=1&page_size=50', method: 'GET', headers: H });
  let d = JSON.parse(k.body);
  let items = d.data?.items || d.data || [];
  
  console.log('=== ALL KNOWLEDGE ===');
  for (const it of items) {
    let p = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/knowledge/' + it.id + '/preview', method: 'GET', headers: H });
    let status = p.code === 200 ? '✅ OK' : '❌ FAIL';
    let errDetail = p.code !== 200 ? p.body.slice(0, 200) : '';
    console.log(`${status} ${it.id} | ${it.title} | ${it.file_path}`);
    if (errDetail) console.log(`   ${errDetail}`);
  }

  // 2. Check /files endpoint for the new file
  console.log('\n=== /files endpoint test ===');
  const newFile = items.find(i => i.file_path && i.file_path.includes('779dc39b'));
  if (newFile) {
    let f = await req({ hostname: 'wiki258.zeabur.app', path: '/files?file_path=' + encodeURIComponent(newFile.file_path), method: 'GET', headers: H });
    console.log('/files:', f.code, 'content-type:', f.headers['content-type']);
    console.log('body start:', f.body.slice(0, 100));
  }

  // 3. Test uploading a small file
  console.log('\n=== Test new upload ===');
  const testContent = Buffer.from('%PDF-1.4 test\n%%EOF');
  const boundary = '----TestBoundary' + Date.now();
  const bodyStart = Buffer.from('--' + boundary + '\r\nContent-Disposition: form-data; name="file"; filename="test-new.pdf"\r\nContent-Type: application/octet-stream\r\n\r\n');
  const bodyEnd = Buffer.from('\r\n--' + boundary + '--\r\n');
  const body = Buffer.concat([bodyStart, testContent, bodyEnd]);
  
  let u = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/knowledge-bases/4b1c1c0a-64d4-4d3b-b605-0f984e66b7c8/knowledge/file', method: 'POST', headers: { 'Authorization': 'Bearer ' + tok, 'Content-Type': 'multipart/form-data; boundary=' + boundary, 'Content-Length': body.length } }, body);
  console.log('Upload:', u.code);
  let uploadData = JSON.parse(u.body);
  if (uploadData.data?.id) {
    let np = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/knowledge/' + uploadData.data.id + '/preview', method: 'GET', headers: H });
    console.log('Preview new upload:', np.code);
    
    // Clean up
    let del = await req({ hostname: 'wiki258.zeabur.app', path: '/api/v1/knowledge/' + uploadData.data.id, method: 'DELETE', headers: H });
    console.log('Cleanup:', del.code);
  }
})();
