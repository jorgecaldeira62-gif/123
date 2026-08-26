console.log('Node.js version:', process.version);
console.log('Current working directory:', process.cwd());

// Check if required modules are available
try {
  require('fs');
  console.log('â fs module available');
} catch (e) {
  console.log('â fs module not available:', e.message);
}

try {
  require('path');
  console.log('â path module available');
} catch (e) {
  console.log('â path module not available:', e.message);
}

try {
  require('pg');
  console.log('â pg module available');
} catch (e) {
  console.log('â pg module not available:', e.message);
}