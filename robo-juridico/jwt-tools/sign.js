const fs  = require('fs');
const jwt = require('jsonwebtoken');

// âââ Uso: node sign.js [caminho/chave_privada.pem] [CPF] ââââââââââââââââââââââ
// Gera um JWT RS256 simples para autenticaÃ§Ã£o no Swagger/HomologaÃ§Ã£o PDPJ.
// Cole o token gerado no campo Authorization do Swagger.

const privateKeyPath = process.argv[2] || 'chave_privada.pem';
const cpf            = process.argv[3] || '00000000000';

if (!fs.existsSync(privateKeyPath)) {
  console.error('â Arquivo de chave privada nÃ£o encontrado:', privateKeyPath);
  console.error('   Uso: node sign.js "C:/caminho/chave_privada.pem" 09494128648');
  process.exit(1);
}

// âââ LÃª e sanitiza a chave PEM ââââââââââââââââââââââââââââââââââââââââââââââââ
let rawKey = fs.readFileSync(privateKeyPath, 'utf8');

// Remove "Bag Attributes" que o OpenSSL Ã s vezes adiciona antes do header PEM
const beginIdx = rawKey.indexOf('-----BEGIN');
if (beginIdx > 0) rawKey = rawKey.slice(beginIdx);

// Corrige chaves sem quebras de linha (exportadas em uma Ãºnica linha)
if (!rawKey.includes('\n') && rawKey.includes('-----')) {
  const bm = rawKey.match(/-----BEGIN [^-]+-----/);
  const em = rawKey.match(/-----END [^-]+-----/);
  if (bm && em) {
    const body = rawKey.replace(bm[0], '').replace(em[0], '').replace(/\s+/g, '');
    rawKey = `${bm[0]}\n${body.replace(/(.{64})/g, '$1\n').trim()}\n${em[0]}`;
  }
}
const privateKey = rawKey.trim();

// âââ Payload padrÃ£o PDPJ âââââââââââââââââââââââââââââââââââââââââââââââââââââ
const payload = {
  sub  : cpf.replace(/\D/g, ''),
  name : 'Maikon da Rocha Caldeira',
  iss  : 'pdpj-br',
  aud  : 'https://gateway.stg.cloud.pje.jus.br',
  iat  : Math.floor(Date.now() / 1000),
  jti  : `sign-${Date.now()}`,
};

// âââ Assina o token RS256 âââââââââââââââââââââââââââââââââââââââââââââââââââââ
try {
  const token = jwt.sign(payload, privateKey, { algorithm: 'RS256', expiresIn: '1h' });
  console.log('\nâ Token JWT gerado com sucesso!\n');
  console.log('ââ Cole no Swagger em "Authorization: Bearer <TOKEN>" ââ');
  console.log(token);
  console.log('ââââââââââââââââââââââââââââââââââââââââââââââââââââââââ\n');
} catch (err) {
  console.error('â Erro ao assinar token:', err.message);
  console.error('   Verifique se a chave PEM estÃ¡ no formato correto (RSA PRIVATE KEY).');
  process.exit(1);
}
