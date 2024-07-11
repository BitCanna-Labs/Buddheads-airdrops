let { bech32 } = require('bech32');
const { writeFileSync, readFileSync } = require('fs');

function processFile(inputFile, outputFile) {
  const tokensOwner = require(inputFile);
  let finalOutput = [];

  for (const type of tokensOwner) {
    const decode = bech32.decode(type.owner);
    const neutaroAddr = bech32.encode('neutaro', decode.words);
    const starAddr = bech32.encode('star', decode.words);

    finalOutput.push({
      "bitcanna": type.owner,
      "startgaze": starAddr,
      "neutaro": neutaroAddr
    });
  }

  try {
    writeFileSync(outputFile, JSON.stringify(finalOutput, null, 2), 'utf8');
    console.log(`Data successfully saved to ${outputFile}`);
  } catch (error) {
    console.log('An error has occurred ', error);
  }
}

processFile('./temporal_stakers_list.json', './final_stakers_list.json');
processFile('./temporal_nostakers_list.json', './final_nostakers_list.json');
