let { bech32 } = require('bech32') 
const { writeFileSync } = require('fs');
const tokensOwner = require('./tokens_with_owners.json');

let finalOutput = []

for (const type of tokensOwner) { 
  const decode = bech32.decode(type.owner);
  const neutaroAddr = bech32.encode('neutaro', decode.words);
  const bitcannaAddr = bech32.encode('bcna', decode.words);
  
  finalOutput.push({    
    "startgaze": type.owner,
    "bitcanna": bitcannaAddr,
    "neutaro": neutaroAddr
  });  
}
 
try {
  writeFileSync('./converted-address.json', JSON.stringify(finalOutput, null, 2), 'utf8');
  console.log('Data successfully saved');
} catch (error) {
  console.log('An error has occurred ', error);
}