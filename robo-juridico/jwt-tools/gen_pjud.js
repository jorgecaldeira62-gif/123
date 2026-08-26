const fs  = require('fs');
const jwt = require('jsonwebtoken');

// âââ Uso ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
// node gen_pjud.js \
//   --key  "caminho/chave_privada.pem" \
//   --sub  "09494128648" \
//   --iss  "https://seu-issuer.pdpj.jus.br" \
//   --aud  "https://gateway.stg.cloud.pje.jus.br" \
//   --name "Maikon da Rocha Caldeira" \
//   --exp  3600 \
//   --out  pjud_token.txt
// âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

// âââ CLI parsing (sem dependÃªncias extras) ââââââââââââââââââââââââââââââââââââ
const argv = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (a.startsWith('--')) {
    argv[a.slice(2)] = process.argv[i + 1];
    i++;
  }
}

// âââ ParÃ¢metros com valores padrÃ£o âââââââââââââââââââââââââââââââââââââââââââ
const keyPath   = argv.key  || argv.k  || 'chave_privada.pem';
const outFile   = argv.out             || 'pjud_token.txt';
const iss       = argv.iss             || 'https://seu-issuer.example';
const aud       = argv.aud             || 'https://gateway.stg.cloud.pje.jus.br';
const sub       = argv.sub             || '00000000000';
const name      = argv.name || argv.nome || '';
const expiresIn = argv.exp  || argv.expires || '5m';

// âââ ValidaÃ§Ãµes âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
if (!fs.existsSync(keyPath)) {
  console.error('â Chave privada nÃ£o encontrada:', keyPath);
  console.error('   Passe o caminho via --key "C:/Users/.../chave_privada.pem"');
  process.exit(1);
}

const cleanSub = sub.replace(/\D/g, '');
if (cleanSub.length !== 11) {
  console.error('â CPF invÃ¡lido. Use --sub 09494128648 (11 dÃ­gitos, sem pontos/traÃ§os)');
  process.exit(1);
}

// âââ LÃª e sanitiza a chave PEM ââââââââââââââââââââââââââââââââââââââââââââââââ
let rawKey = fs.readFileSync(keyPath, 'utf8');

const beginIdx = rawKey.indexOf('-----BEGIN');
if (beginIdx > 0) rawKey = rawKey.slice(beginIdx);

if (!rawKey.includes('\n') && rawKey.includes('-----')) {
  const beginMatch = rawKey.match(/-----BEGIN [^-]+-----/);
  const endMatch   = rawKey.match(/-----END [^-]+-----/);
  if (beginMatch && endMatch) {
    const header = beginMatch[0];
    const footer = endMatch[0];
    const body   = rawKey.replace(header, '').replace(footer, '').replace(/\s+/g, '');
    rawKey = `${header}\n${body.replace(/(.{64})/g, '$1\n').trim()}\n${footer}`;
  }
}
const key = rawKey.trim();

// âââ Monta payload ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
const now     = Math.floor(Date.now() / 1000);
const payload = { sub: cleanSub, iss, aud, iat: now, jti: `pjud-${Date.now()}` };
if (name) payload.name = name;

// âââ Resolve expiresIn (aceita '5m', '1h', '300') ââââââââââââââââââââââââââââ
const expVal = /^\d+$/.test(expiresIn) ? parseInt(expiresIn, 10) : expiresIn;

// âââ Assina e salva âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
try {
  const token = jwt.sign(payload, key, { algorithm: 'RS256', expiresIn: expVal });
  fs.writeFileSync(outFile, token);

  const expSeg = typeof expVal === 'number' ? expVal : 300;
  console.log(`\nâ Token criado e salvo em: ${outFile}`);
  console.log('\nPayload:');
  console.log(JSON.stringify({ ...payload, exp: now + expSeg }, null, 2));
  console.log('\nToken (primeiros 80 chars):');
  console.log(token.substring(0, 80) + '...\n');
} catch (err) {
  console.error('â Erro ao assinar token:', err.message);
  process.exit(1);
}
