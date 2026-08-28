const fs = require('fs');
const path = require('path');

// Check the web/ directory's main JS bundle for the old postUpload code
const webDir = 'd:\\WeKnora\\web\\assets';
const files = fs.readdirSync(webDir);
const mainBundle = files.find(f => f.startsWith('index-') && f.endsWith('.js'));
console.log('Main bundle:', mainBundle);

if (mainBundle) {
  const content = fs.readFileSync(path.join(webDir, mainBundle), 'utf-8');
  
  // Check for old hardcoded Content-Type
  const hasOldCode = content.includes('"Content-Type":"multipart/form-data"') || 
                     (content.includes('Content-Type') && content.includes('multipart/form-data') && content.includes('postUpload'));
  console.log('Has old Content-Type hardcode:', hasOldCode);
  
  // Find the postUpload function
  const postUploadMatch = content.match(/postUpload[\s\S]{0,300}/);
  if (postUploadMatch) {
    console.log('\npostUpload context:');
    // Show the relevant part
    const idx = content.indexOf('postUpload');
    console.log(content.slice(idx, idx + 300));
  }
}

// Also check if frontend/dist has the newer code
const distDir = 'd:\\WeKnora\\frontend\\dist\\assets';
if (fs.existsSync(distDir)) {
  const distFiles = fs.readdirSync(distDir);
  const distBundle = distFiles.find(f => f.startsWith('index-') && f.endsWith('.js'));
  console.log('\nDist bundle:', distBundle);
  
  if (distBundle) {
    const distContent = fs.readFileSync(path.join(distDir, distBundle), 'utf-8');
    const distHasOldCode = distContent.includes('"Content-Type":"multipart/form-data"');
    console.log('Dist has old Content-Type hardcode:', distHasOldCode);
  }
}
