const fs = require('fs');

// âââ Uso ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
// node call_pjud.js --url <API_URL> [--tokenfile pjud_token.txt] [--method GET]
//
// Exemplos:
//   node call_pjud.js --url "https://gateway.stg.cloud.pje.jus.br/domicilio-eletronico/api/v1/representados"
//   node call_pjud.js --url "https://comunicaapi.pje.jus.br/api/v1/comunicacao" --tokenfile pjud_token.txt
//
// Requer Node.js 18+ (fetch global nativo).
// âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

const argv = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) {
    argv[a.slice(2)] = process.argv[i + 1];
    i++;
  }
}

const url       = argv.url || argv.u;
const tokenFile = argv.tokenfile || argv.t || 'pjud_token.txt';
const method    = (argv.method || 'GET').toUpperCase();

if (!url) {
  console.error('â URL obrigatÃ³ria. Uso:');
  console.error('   node call_pjud.js --url <API_URL> [--tokenfile pjud_token.txt] [--method GET|POST]');
  process.exit(1);
}

if (!fs.existsSync(tokenFile)) {
  console.error(`â Arquivo de token nÃ£o encontrado: ${tokenFile}`);
  console.error('   Gere o token primeiro com:');
  console.error('   node gen_pjud.js --key chave_privada.pem --sub 09494128648');
  process.exit(1);
}

// LÃª o token ignorando comentÃ¡rios e linhas extras
const raw   = fs.readFileSync(tokenFile, 'utf8');
const token = raw
  .split('\n')
  .map(l => l.trim())
  .filter(l => l && !l.startsWith('#') && !l.startsWith('curl') && !l.startsWith('-'))
  .join('')
  .trim();

if (!token || token.split('.').length !== 3) {
  console.error('â Token JWT invÃ¡lido ou arquivo corrompido.');
  console.error('   Regenere com: node gen_pjud.js --key chave_privada.pem --sub 09494128648');
  console.error('   Token lido (60 chars):', token ? token.substring(0, 60) : '(vazio)');
  process.exit(1);
}

console.log(`\nð¡ ${method} ${url}`);
console.log(`ð Token: ${token.substring(0, 40)}...\n`);

(async () => {
  try {
    const res = await fetch(url, {
      method,
      headers: {
        'Authorization' : `Bearer ${token}`,
        'Accept'        : 'application/json',
        'Content-Type'  : 'application/json',
      },
    });

    const text = await res.text();
    console.log('ââ Resposta âââââââââââââââââââââââââââââââââââââââââ');
    console.log(`Status: ${res.status} ${res.statusText}`);

    if (res.status === 401) {
      console.error('\nâ ï¸  401 Unauthorized');
      console.error('   â O token pode estar expirado ou a chave nÃ£o estÃ¡ registrada no PDPJ.');
      console.error('   â Regenere: node gen_pjud.js --key chave_privada.pem --sub 09494128648');
    } else if (res.status === 403) {
      console.error('\nâ ï¸  403 Forbidden');
      console.error('   â PossÃ­vel restriÃ§Ã£o de IP. Use um servidor brasileiro.');
    }

    try {
      const json = JSON.parse(text);
      console.log(JSON.stringify(json, null, 2));
    } catch {
      console.log(text);
    }
  } catch (err) {
    console.error('â Falha na requisiÃ§Ã£o:', err.message || err);
    process.exit(1);
  }
})();
